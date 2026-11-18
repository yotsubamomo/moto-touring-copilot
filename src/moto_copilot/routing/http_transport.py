"""The real HTTPS transport of the routing engine client (SPEC-R1 R1-4 scope (a); CL-R1-25).

`https_transport(url, body, headers)` fits the `Transport` interface of valhalla.py and sends
exactly one HTTPS POST with the standard library's `http.client.HTTPSConnection`. `valhalla_client()`
builds a `ValhallaClient` that uses it with the default endpoint `VALHALLA_ENDPOINT`.

This is the only module of the routing package that may use the network, and no other module of
the package imports it (`__init__.py` included): `import moto_copilot.routing`, hashing, storage,
selection and the adoption checks load no network module. A caller that needs the real transport
imports `moto_copilot.routing.http_transport` explicitly.

The endpoint cannot be redirected (CL-R1-25 item 2; H-1):
- no redirect is followed: one connection and one request per call; a 3xx reply is returned as it
  is, and the client never adopts a reply that is not 200;
- no proxy is used: `set_tunnel` is never called; this module reads no env variables, and no
  env variable changes the host, the port, a proxy or a redirect; `urllib.request` is not used (it
  follows redirects and takes proxies from the env);
- the URL is checked again here: `https://` plus a host (and port) plus `/route`,
  `/trace_attributes` or `/status`, nothing else; the connection goes only to that host and port;
- TLS verification is always on and there is no switch to turn it off. The context is built with
  explicit settings (CL-R1-28, decision-20261118-issue16-c2r1f3): `ssl.SSLContext(PROTOCOL_TLS_CLIENT)`,
  certificates required, hostname check on, then `load_default_certs(Purpose.SERVER_AUTH)`. It is
  not `ssl.create_default_context()`, so it does not consult `SSLKEYLOGFILE` and no TLS secrets
  are written to a file. Loading the default trust store lets OpenSSL consult `SSL_CERT_FILE` and
  `SSL_CERT_DIR`; those can only add trusted root certificates and do not change the host or the
  port (TI-C2R1F3-1);
- a fixed timeout, `TIMEOUT_S`, and no retry.

Content (CL-R1-25 item 3; H-2): the body is sent as the client gave it; the only headers are the
client's `Content-Type` and `User-Agent`, plus the `Host`, `Content-Length` and `Accept-Encoding`
that `http.client` adds. Any failure to connect, send or read becomes `TransportError` with a fixed
message, raised `from None` (no request body, coordinate, shape or reply body in it). HTTP error
statuses (4xx, 5xx) are replies, not exceptions. Nothing here logs, prints, writes a file or keeps
a request or a reply.
"""
from __future__ import annotations

import http.client
import re
import ssl
from collections.abc import Callable, Mapping
from datetime import datetime

from .valhalla import VALHALLA_ENDPOINT, HttpResponse, TransportError, ValhallaClient

TIMEOUT_S = 30.0  # seconds, for connecting and for each read (CL-R1-25 item 2 (e))
PATHS = ("/route", "/trace_attributes", "/status")
ALLOWED_HEADERS = ("Content-Type", "User-Agent")

# The host and port rule of valhalla.py's endpoint check, followed by one of the three paths.
_URL = re.compile(
    r"https://(?P<host>[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?)(?::(?P<port>[0-9]{1,5}))?"
    r"(?P<path>/route|/trace_attributes|/status)"
)


def _target(url) -> tuple[str, int | None, str]:
    """(host, port or None for 443, path) of an accepted URL; ValueError otherwise (no connection made)."""
    match = _URL.fullmatch(url) if isinstance(url, str) else None
    if match is None:
        raise ValueError("the transport accepts only https://<host>[:port] with /route, /trace_attributes or /status")
    port = match.group("port")
    if port is not None and not 1 <= int(port) <= 65535:
        raise ValueError("the port of the URL is out of range")
    return match.group("host"), None if port is None else int(port), match.group("path")


def _headers(headers) -> dict[str, str]:
    if not isinstance(headers, Mapping) or not set(headers) <= set(ALLOWED_HEADERS):
        raise ValueError("the transport sends only the Content-Type and User-Agent headers")
    if not all(isinstance(value, str) for value in headers.values()):
        raise ValueError("header values must be strings")
    return dict(headers)


def _tls_context() -> ssl.SSLContext:
    """The TLS client context (CL-R1-28 item 2): verification required, hostname check on."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs(ssl.Purpose.SERVER_AUTH)
    return context


def https_transport(url: str, body: bytes, headers: Mapping[str, str]) -> HttpResponse:
    """Send one HTTPS POST of `body` to `url` and return the status and body of the reply."""
    host, port, path = _target(url)
    if not isinstance(body, bytes):
        raise TypeError("the request body must be bytes")
    sent_headers = _headers(headers)
    context = _tls_context()
    connection = None
    failed = False
    try:
        connection = http.client.HTTPSConnection(host, port, timeout=TIMEOUT_S, context=context)
        connection.request("POST", path, body=body, headers=sent_headers)
        reply = connection.getresponse()
        status = reply.status
        data = reply.read()
    except (OSError, http.client.HTTPException):
        failed = True
    finally:
        if connection is not None:
            connection.close()
    if failed:
        # Raised outside the except block and from None: no chained error carries the request.
        raise TransportError("the routing engine could not be reached") from None
    return HttpResponse(status, data)


def valhalla_client(*, endpoint: str = VALHALLA_ENDPOINT,
                    clock: Callable[[], datetime] | None = None) -> ValhallaClient:
    """A ValhallaClient that sends its requests with `https_transport` (default endpoint VALHALLA_ENDPOINT)."""
    return ValhallaClient(https_transport, endpoint=endpoint, clock=clock)
