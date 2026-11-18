"""SPEC-R1 R1-4 (Issue #16): the real HTTPS transport, routing/http_transport.py (CL-R1-25).

No test sends a network request. `http.client.HTTPSConnection` is replaced with stand-ins:
- `Scripted`: records the constructor arguments, the request, `set_tunnel` and `close`, and
  answers from a script (or raises at a chosen stage);
- `Wire`: the real `HTTPSConnection` with `connect` replaced, so http.client itself writes the
  request bytes into an in-memory socket and parses a canned reply from it.
An autouse fixture also makes every socket call fail. All bodies, positions and replies are
synthetic (see tests/test_routing_engine.py); host names in replies use the reserved `.invalid`.
"""
from __future__ import annotations

import http.client
import io
import json
import os
import socket
import ssl
import subprocess
import sys
import traceback
from pathlib import Path

import pytest

from moto_copilot.routing import (
    ROUTING_UNAVAILABLE,
    USER_AGENT,
    VALHALLA_ENDPOINT,
    AdoptedRoute,
    HttpResponse,
    RouteFailure,
    SnapshotStore,
    TransportError,
    ValhallaClient,
    get_route,
)
from moto_copilot.routing import http_transport
from moto_copilot.routing.http_transport import TIMEOUT_S, https_transport, valhalla_client

import test_routing_engine as eng

HOST = "valhalla1.openstreetmap.de"
SECRET = "0.0123456789"  # a synthetic coordinate string that must never reach a message


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)


class Recorder:
    def __init__(self):
        self.made = []
        self.answers = []       # (status, body bytes)
        self.fail_at = None     # "init", "request", "getresponse" or "read"
        self.error = None


class Reply:
    def __init__(self, status, body, recorder):
        self.status, self._body, self._recorder = status, body, recorder

    def read(self):
        if self._recorder.fail_at == "read":
            raise self._recorder.error
        return self._body


def scripted(recorder: Recorder):
    class Scripted:
        def __init__(self, host, port=None, timeout=None, context=None, **kwargs):
            self.host, self.port, self.timeout, self.context, self.kwargs = host, port, timeout, context, kwargs
            self.requests, self.tunnel, self.closed = [], None, False
            recorder.made.append(self)
            if recorder.fail_at == "init":
                raise recorder.error

        def set_tunnel(self, *args, **kwargs):
            self.tunnel = (args, kwargs)

        def request(self, method, url, body=None, headers=None, **kwargs):
            self.requests.append((method, url, body, dict(headers or {}), kwargs))
            if recorder.fail_at == "request":
                raise recorder.error

        def getresponse(self):
            if recorder.fail_at == "getresponse":
                raise recorder.error
            status, body = recorder.answers.pop(0)
            return Reply(status, body, recorder)

        def close(self):
            self.closed = True

    return Scripted


@pytest.fixture
def conn(monkeypatch) -> Recorder:
    recorder = Recorder()
    monkeypatch.setattr(http.client, "HTTPSConnection", scripted(recorder))
    return recorder


class WireSock:
    def __init__(self, reply: bytes):
        self.sent = b""
        self.reply = reply

    def sendall(self, data):
        self.sent += bytes(data)

    def makefile(self, mode, *args, **kwargs):
        return io.BytesIO(self.reply)

    def close(self):
        pass


@pytest.fixture
def wire(monkeypatch):
    real = http.client.HTTPSConnection
    state = {"replies": [], "socks": [], "made": []}

    class Wire(real):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            state["made"].append(self)

        def connect(self):
            self.sock = WireSock(state["replies"].pop(0))
            state["socks"].append(self.sock)

    def factory(*args, **kwargs):
        # http.client's HTTPSConnection.__init__ calls super() by the module-level name, so the
        # real class is put back while the stand-in is built.
        http.client.HTTPSConnection = real
        try:
            return Wire(*args, **kwargs)
        finally:
            http.client.HTTPSConnection = factory

    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    return state


def raw_reply(status: int, reason: str, body: bytes = b"{}", extra: str = "") -> bytes:
    return (f"HTTP/1.1 {status} {reason}\r\n{extra}Content-Length: {len(body)}\r\n\r\n").encode("ascii") + body


def parse_sent(data: bytes):
    head, _, body = data.partition(b"\r\n\r\n")
    lines = head.decode("ascii").split("\r\n")
    headers = dict(line.split(": ", 1) for line in lines[1:])
    return lines[0], headers, body


CLIENT_HEADERS = {"Content-Type": "application/json", "User-Agent": USER_AGENT}


# --- T-1 redirects -------------------------------------------------------------------------------

@pytest.mark.parametrize("status", [301, 302, 303, 307, 308])
def test_t1_a_redirect_is_returned_as_it_is_and_not_followed(wire, status):
    wire["replies"].append(raw_reply(status, "Moved", b"{}", "Location: https://elsewhere.invalid/route\r\n"))
    result = https_transport(f"{VALHALLA_ENDPOINT}/route", b"{}", CLIENT_HEADERS)
    assert result == HttpResponse(status, b"{}")
    assert len(wire["made"]) == 1 and len(wire["socks"]) == 1
    assert wire["made"][0].host == HOST
    request_line, _, _ = parse_sent(wire["socks"][0].sent)
    assert request_line == "POST /route HTTP/1.1"


def test_t1_a_redirected_route_request_is_routing_unavailable_with_no_snapshot(conn, tmp_path):
    conn.answers = [(302, b'{"moved": true}'), (302, b'{"moved": true}')]
    client = valhalla_client(clock=eng.Clock())
    result = get_route(eng.engine_request(), store=SnapshotStore(tmp_path), client=client, now=eng.NOW)
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:engine_error", "return:engine_error"))
    assert list(tmp_path.iterdir()) == []
    assert [c.host for c in conn.made] == [HOST, HOST] and all(len(c.requests) == 1 for c in conn.made)


# --- T-2 proxies and env variables ---------------------------------------------------------------

def test_t2_proxies_and_endpoint_variables_do_not_change_the_connection(tmp_path):
    code = (
        "import http.client, json\n"
        "seen = []\n"
        "class Fake:\n"
        "    def __init__(self, host, port=None, timeout=None, context=None, **kw):\n"
        "        self.entry = {'host': host, 'port': port, 'tunnel': None}\n"
        "        seen.append(self.entry)\n"
        "    def set_tunnel(self, *a, **k):\n"
        "        self.entry['tunnel'] = [list(a), k]\n"
        "    def request(self, method, url, body=None, headers=None, **kw):\n"
        "        self.entry['path'] = url\n"
        "    def getresponse(self):\n"
        "        class R:\n"
        "            status = 200\n"
        "            def read(self):\n"
        "                return b'{\"version\": \"0.0.0-synthetic\"}'\n"
        "        return R()\n"
        "    def close(self):\n"
        "        pass\n"
        "http.client.HTTPSConnection = Fake\n"
        "from moto_copilot.routing.http_transport import valhalla_client\n"
        "client = valhalla_client()\n"
        "reply = client.status()\n"
        "print(json.dumps({'endpoint': client.endpoint, 'seen': seen, 'status': reply.status}))\n"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    marker = "http://proxy.invalid:3128"
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy",
                 "no_proxy", "VALHALLA_URL", "VALHALLA_ENDPOINT", "VALHALLA_HOST", "ROUTING_ENDPOINT", "ROUTING_URL"):
        env[name] = marker if "PROXY" in name.upper() else "https://redirected.invalid"
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8",
                          env=env, timeout=60, cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    report = json.loads(done.stdout)
    assert report == {"endpoint": VALHALLA_ENDPOINT, "status": 200,
                      "seen": [{"host": HOST, "port": None, "tunnel": None, "path": "/status"}]}


# --- T-3 TLS; T-4 timeout ------------------------------------------------------------------------

def test_t3_tls_verification_is_on(conn):
    conn.answers = [(200, b"{}")]
    https_transport(f"{VALHALLA_ENDPOINT}/status", b"{}", CLIENT_HEADERS)
    context = conn.made[0].context
    assert isinstance(context, ssl.SSLContext)
    assert context.check_hostname is True and context.verify_mode == ssl.CERT_REQUIRED
    assert conn.made[0].tunnel is None and conn.made[0].kwargs == {}


def test_t3_the_transport_has_no_switch_for_tls_or_proxies():
    import inspect
    assert list(inspect.signature(https_transport).parameters) == ["url", "body", "headers"]
    source = Path(http_transport.__file__).read_text(encoding="utf-8")
    for text in ("CERT_NONE", "check_hostname = False", "_create_unverified_context", "set_tunnel(",
                 "urlopen", "import urllib"):
        assert text not in source


def test_t4_the_timeout_is_the_fixed_constant(conn):
    conn.answers = [(200, b"{}")]
    https_transport(f"{VALHALLA_ENDPOINT}/route", b"{}", CLIENT_HEADERS)
    assert conn.made[0].timeout == TIMEOUT_S
    assert isinstance(TIMEOUT_S, float) and 0 < TIMEOUT_S < float("inf")


def test_t4_a_timeout_is_a_transport_error(conn):
    conn.fail_at, conn.error = "getresponse", TimeoutError("timed out")
    with pytest.raises(TransportError):
        https_transport(f"{VALHALLA_ENDPOINT}/route", b"{}", CLIENT_HEADERS)
    assert len(conn.made) == 1 and conn.made[0].closed


# --- T-5 failures --------------------------------------------------------------------------------

ERRORS = [
    OSError(f"synthetic failure near {SECRET}"),
    ConnectionRefusedError(f"refused {SECRET}"),
    ssl.SSLError(f"synthetic tls {SECRET}"),
    http.client.RemoteDisconnected(f"closed {SECRET}"),
    http.client.IncompleteRead(SECRET.encode("ascii")),
]


@pytest.mark.parametrize("stage", ["init", "request", "getresponse", "read"])
@pytest.mark.parametrize("error", ERRORS, ids=lambda e: type(e).__name__)
def test_t5_every_failure_is_a_transport_error_without_content(conn, stage, error):
    conn.fail_at, conn.error = stage, error
    conn.answers = [(200, b"{}")]
    body = json.dumps({"locations": [{"lat": float(SECRET), "lon": float(SECRET), "type": "break"}]}).encode()
    with pytest.raises(TransportError) as exc:
        https_transport(f"{VALHALLA_ENDPOINT}/route", body, CLIENT_HEADERS)
    assert len(conn.made) == 1  # no second connection: no retry
    assert all(len(c.requests) <= 1 for c in conn.made)
    if stage != "init":
        assert conn.made[0].closed
    text = "".join(traceback.format_exception(exc.value))
    assert SECRET not in text and "locations" not in text
    assert exc.value.__cause__ is None and exc.value.__context__ is None


def test_t5_a_failure_through_the_client_keeps_positions_out_of_the_message(conn, tmp_path):
    conn.fail_at, conn.error = "request", OSError("synthetic")
    client = valhalla_client(clock=eng.Clock())
    result = get_route(eng.engine_request(), store=SnapshotStore(tmp_path), client=client, now=eng.NOW)
    assert result == RouteFailure(ROUTING_UNAVAILABLE, None, ("outbound:engine_unreachable", "return:not_sent"))
    assert len(conn.made) == 1 and list(tmp_path.iterdir()) == []


# --- T-6 content and headers ---------------------------------------------------------------------

@pytest.mark.parametrize("path", ["/route", "/trace_attributes", "/status"])
def test_t6_the_wire_request_is_a_post_with_the_given_body_and_only_the_listed_headers(wire, path):
    body = json.dumps({"synthetic": [1.5, 2.25]}, separators=(",", ":")).encode("utf-8")
    wire["replies"].append(raw_reply(200, "OK", b'{"ok":1}'))
    result = https_transport(f"{VALHALLA_ENDPOINT}{path}", body, CLIENT_HEADERS)
    assert result == HttpResponse(200, b'{"ok":1}')
    request_line, headers, sent_body = parse_sent(wire["socks"][0].sent)
    assert request_line == f"POST {path} HTTP/1.1"
    assert sent_body == body
    assert set(headers) == {"Host", "Accept-Encoding", "Content-Length", "Content-Type", "User-Agent"}
    assert headers["Host"] == HOST and headers["Content-Length"] == str(len(body))
    assert headers["Content-Type"] == "application/json" and headers["User-Agent"] == USER_AGENT
    assert headers["Accept-Encoding"] == "identity"


def test_t6_the_client_requests_reach_the_wire_unchanged(wire):
    sent = []

    def recording(url, body, headers):
        sent.append(body)
        return https_transport(url, body, headers)

    wire["replies"].append(raw_reply(200, "OK", json.dumps(eng.STATUS).encode()))
    ValhallaClient(recording).status()
    assert parse_sent(wire["socks"][0].sent)[2] == sent[0] == b"{}"


@pytest.mark.parametrize("headers", [
    {"Content-Type": "application/json", "User-Agent": USER_AGENT, "Cookie": "x=1"},
    {"Authorization": "Bearer synthetic"},
    {"User-Agent": 1},
    "User-Agent: x",
])
def test_t6_headers_outside_the_closed_list_are_refused_before_connecting(conn, headers):
    with pytest.raises(ValueError):
        https_transport(f"{VALHALLA_ENDPOINT}/route", b"{}", headers)
    assert conn.made == []


def test_t6_the_body_must_be_bytes(conn):
    with pytest.raises(TypeError):
        https_transport(f"{VALHALLA_ENDPOINT}/route", "{}", CLIENT_HEADERS)
    assert conn.made == []


# --- T-7 URL checks ------------------------------------------------------------------------------

@pytest.mark.parametrize("url", [
    f"http://{HOST}/route",
    f"https://user@{HOST}/route",
    f"https://{HOST}/route?x=1",
    f"https://{HOST}/route#x",
    f"https://{HOST}",
    f"https://{HOST}/",
    f"https://{HOST}/locate",
    f"https://{HOST}/route/extra",
    f"https://{HOST}/route\n",
    f"https://{HOST}:99999/route",
    f"https://{HOST}:0/route",
    "https:///route",
    None,
])
def test_t7_urls_other_than_the_three_actions_are_refused_before_connecting(conn, url):
    with pytest.raises(ValueError):
        https_transport(url, b"{}", CLIENT_HEADERS)
    assert conn.made == []


def test_t7_an_explicit_port_is_used(conn):
    conn.answers = [(200, b"{}")]
    https_transport("https://engine.example:8002/status", b"{}", CLIENT_HEADERS)
    assert (conn.made[0].host, conn.made[0].port) == ("engine.example", 8002)


# --- T-8 HTTP error statuses ---------------------------------------------------------------------

@pytest.mark.parametrize("status, reason", [(400, "Bad Request"), (404, "Not Found"), (429, "Too Many Requests"),
                                            (500, "Internal Server Error"), (503, "Service Unavailable")])
def test_t8_http_error_statuses_are_replies_not_exceptions(wire, status, reason):
    wire["replies"].append(raw_reply(status, reason, b'{"error":"synthetic"}'))
    assert https_transport(f"{VALHALLA_ENDPOINT}/route", b"{}", CLIENT_HEADERS) == HttpResponse(status, b'{"error":"synthetic"}')
    assert len(wire["made"]) == 1


# --- T-9 the real-transport client ---------------------------------------------------------------

def test_t9_valhalla_client_uses_the_real_transport_and_the_default_endpoint():
    client = valhalla_client()
    assert client.endpoint == VALHALLA_ENDPOINT
    assert client._transport is https_transport


def test_t9_a_round_trip_through_the_real_transport_equals_the_fake_engine(conn, tmp_path):
    replies = {
        "/route": [eng.route_body(eng.OUT_POINTS), eng.route_body(eng.BACK_POINTS)],
        "/trace_attributes": [eng.trace_body(eng.OUT_POINTS), eng.trace_body(eng.BACK_POINTS)],
        "/status": [eng.STATUS],
    }
    order = ["/route", "/trace_attributes", "/route", "/trace_attributes", "/status"]
    conn.answers = [(200, json.dumps(replies[path].pop(0), ensure_ascii=False).encode("utf-8")) for path in order]
    first_dir, second_dir = tmp_path / "a", tmp_path / "b"
    first_dir.mkdir()
    second_dir.mkdir()
    real = get_route(eng.engine_request(), store=SnapshotStore(first_dir), client=valhalla_client(clock=eng.Clock()),
                     now=eng.NOW)
    fake = get_route(eng.engine_request(), store=SnapshotStore(second_dir),
                     client=ValhallaClient(eng.round_trip_engine(), clock=eng.Clock()), now=eng.NOW)
    assert isinstance(real, AdoptedRoute) and real == fake
    assert [c.requests[0][1] for c in conn.made] == order
    assert {p.name: p.read_bytes() for p in first_dir.iterdir()} == {p.name: p.read_bytes() for p in second_dir.iterdir()}


# --- the package does not load the transport -----------------------------------------------------

def test_importing_the_routing_package_does_not_load_the_transport(tmp_path):
    code = (
        "import json, sys\n"
        "import moto_copilot.routing\n"
        "from moto_copilot.routing import get_route, ValhallaClient\n"
        "print(json.dumps('moto_copilot.routing.http_transport' in sys.modules))\n"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8",
                          env=env, timeout=60, cwd=tmp_path)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) is False
