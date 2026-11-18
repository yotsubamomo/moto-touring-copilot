"""Client of the public Valhalla routing server (SPEC-R1 R1-4 scope (a); CL-R1-5, CL-R1-9).

Endpoint (CL-R1-9; H-1): `VALHALLA_ENDPOINT` is a constant of this module. A caller may pass
another endpoint explicitly to `ValhallaClient`; nothing in this package reads process settings
or env variables, so the endpoint cannot be redirected from outside the program.

Identification (CL-R1-9; H-2): `USER_AGENT` is a generic client name. It holds no person's name,
no email address and no project name.

Transport: the caller gives a `transport` callable that sends one HTTP POST and returns an
`HttpResponse` (status and body bytes), or raises `TransportError` when no response arrives.
This module never opens a connection itself; tests replace the transport with doubles.

Requests (CL-R1-5):
- route: only the positions of one direction (latitude, longitude and the location type, in
  order) and the fixed routing parameters: motorcycle costing with `use_highways: 0`. No hard
  exclusion is sent and no elevation is asked for. Codes, roles and names stay in the program.
- trace_attributes (the road attribute query of SPEC-001 7.11 item 5): only the engine's own
  encoded shape plus the query parameters.
- status: an empty request; the reply gives the engine version (DD-R1-2).

Nothing here retries a request, logs, or keeps a request or a response. Error messages never
hold a coordinate or a shape.
"""
from __future__ import annotations

import copy
import json
import math
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime

from .snapshot import TAIPEI

ENGINE_NAME = "Valhalla"
VALHALLA_ENDPOINT = "https://valhalla1.openstreetmap.de"
USER_AGENT = "route-client/1.0"

# SPEC-001 4.14 routing_params: what is sent besides the positions (P-1: use_highways 0, no
# hard exclusion; Q-3 item 7: no elevation).
_ROUTING_PARAMS = {
    "costing": "motorcycle",
    "costing_options": {"motorcycle": {"use_highways": 0}},
    "units": "kilometers",
}
# The start and the end of a direction are stops; every intermediate position is a "via": the
# route passes it (a U-turn is allowed there) without splitting the route into several legs, so
# one direction is one leg with one shape.
END_LOCATION_TYPE = "break"
INTERMEDIATE_LOCATION_TYPE = "via"

TRACE_ATTRIBUTES = ("edge.names", "edge.length", "edge.road_class")
TRACE_SHAPE_MATCH = "walk_or_snap"

_ENDPOINT = re.compile(r"https://[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?(?::[0-9]{1,5})?")


def routing_params() -> dict:
    """A fresh copy of the fixed routing parameters (CL-R1-5)."""
    return copy.deepcopy(_ROUTING_PARAMS)


class TransportError(Exception):
    """No HTTP response arrived (the engine could not be reached)."""


@dataclass(frozen=True)
class HttpResponse:
    status: int
    body: bytes


Transport = Callable[[str, bytes, Mapping[str, str]], HttpResponse]


@dataclass(frozen=True)
class Position:
    """One request position of a direction (CL-R1-5): code, role and coordinates."""

    ref_id: str
    role: str
    lat: float
    lon: float


def position_from(value) -> Position:
    """A Position from a mapping with ref_id, role, lat and lon. Messages never hold coordinates."""
    if isinstance(value, Position):
        value = {"ref_id": value.ref_id, "role": value.role, "lat": value.lat, "lon": value.lon}
    if not isinstance(value, Mapping):
        raise ValueError("a request position must be an object with ref_id, role, lat and lon")
    ref_id, role = value.get("ref_id"), value.get("role")
    if not isinstance(ref_id, str) or ref_id == "":
        raise ValueError("a request position needs a non-empty ref_id")
    if not isinstance(role, str) or role == "":
        raise ValueError("a request position needs a non-empty role")
    lat, lon = value.get("lat"), value.get("lon")
    for name, number, limit in (("lat", lat, 90.0), ("lon", lon, 180.0)):
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            raise ValueError(f"the {name} of a request position must be a number")
        if not math.isfinite(number) or abs(number) > limit:
            raise ValueError(f"the {name} of a request position is out of range")
    # CL-R1-19 item 2: coordinates are floats (121 becomes 121.0).
    return Position(ref_id, role, float(lat), float(lon))


def route_locations(positions: Sequence[Position]) -> list[dict]:
    """The `locations` sent for one direction: lat, lon and type only, in the given order."""
    last = len(positions) - 1
    return [
        {
            "lat": p.lat,
            "lon": p.lon,
            "type": END_LOCATION_TYPE if i in (0, last) else INTERMEDIATE_LOCATION_TYPE,
        }
        for i, p in enumerate(positions)
    ]


def route_body(positions: Sequence[Position]) -> dict:
    """The body of one route request (CL-R1-5)."""
    if len(positions) < 2:
        raise ValueError("a direction needs at least a start and an end position")
    return {"locations": route_locations(positions), **routing_params()}


def trace_body(shape: str) -> dict:
    """The body of the road attribute query: the engine's own shape, nothing else of the request."""
    if not isinstance(shape, str) or shape == "":
        raise ValueError("the road attribute query needs the encoded shape")
    return {
        "encoded_polyline": shape,
        "costing": _ROUTING_PARAMS["costing"],
        "shape_match": TRACE_SHAPE_MATCH,
        "filters": {"attributes": list(TRACE_ATTRIBUTES), "action": "include"},
    }


@dataclass(frozen=True)
class EngineReply:
    """One HTTP response: the status, the parsed JSON body (None when it is not JSON) and when it arrived."""

    status: int
    body: object
    received_at: datetime


def _reject_constant(_name):
    raise ValueError("NaN and infinities are not JSON")


def _parse_json(data: bytes):
    try:
        return json.loads(data.decode("utf-8"), parse_constant=_reject_constant)
    except (UnicodeDecodeError, ValueError, RecursionError):
        return None


def _default_clock() -> datetime:
    return datetime.now(TAIPEI)


class ValhallaClient:
    """One client of the routing engine. Each call sends exactly one request; nothing is retried."""

    def __init__(self, transport: Transport, *, endpoint: str = VALHALLA_ENDPOINT,
                 clock: Callable[[], datetime] | None = None):
        if not callable(transport):
            raise TypeError("transport must be callable")
        if not isinstance(endpoint, str) or _ENDPOINT.fullmatch(endpoint) is None:
            raise ValueError("endpoint must be an https URL with a host and nothing after it")
        self._transport = transport
        self.endpoint = endpoint
        self._clock = clock or _default_clock

    def _post(self, action: str, payload: dict) -> EngineReply:
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        response = self._transport(f"{self.endpoint}/{action}", data, headers)
        received_at = self._clock()
        if not isinstance(response, HttpResponse):
            raise TypeError("the transport must return an HttpResponse")
        if isinstance(response.status, bool) or not isinstance(response.status, int) or not isinstance(response.body, bytes):
            raise TypeError("the transport returned an HttpResponse with a bad status or body type")
        if not isinstance(received_at, datetime) or received_at.utcoffset() is None:
            raise ValueError("the clock must return a timezone-aware datetime")
        return EngineReply(response.status, _parse_json(response.body), received_at)

    def route(self, positions: Sequence[Position]) -> EngineReply:
        """One route request for one direction. Raises TransportError when no response arrives."""
        return self._post("route", route_body(positions))

    def trace_attributes(self, shape: str) -> EngineReply:
        """One road attribute query on the engine's own shape. Raises TransportError when no response arrives."""
        return self._post("trace_attributes", trace_body(shape))

    def status(self) -> EngineReply:
        """One status request (engine version; DD-R1-2). Raises TransportError when no response arrives."""
        return self._post("status", {})


class PolylineError(ValueError):
    """An encoded shape cannot be decoded. The message never holds the shape."""


def decode_polyline6(shape: str) -> list[tuple[float, float]]:
    """A Valhalla encoded polyline (six decimal places) as [(lat, lon)], in order."""
    if not isinstance(shape, str) or shape == "":
        raise PolylineError("the shape must be a non-empty string")
    out: list[tuple[float, float]] = []
    i, lat, lon, n = 0, 0, 0, len(shape)
    while i < n:
        deltas = []
        for _ in range(2):
            shift = result = 0
            while True:
                if i >= n:
                    raise PolylineError("the shape ends inside a value")
                b = ord(shape[i]) - 63
                i += 1
                if not 0 <= b <= 63:
                    raise PolylineError("the shape holds a character outside the polyline alphabet")
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            deltas.append(~(result >> 1) if result & 1 else result >> 1)
        lat += deltas[0]
        lon += deltas[1]
        point = (lat / 1e6, lon / 1e6)
        if abs(point[0]) > 90.0 or abs(point[1]) > 180.0:
            raise PolylineError("the shape holds a position out of range")
        out.append(point)
    return out
