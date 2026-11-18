"""Geometry-only GPX reading for the target route GPX (SPEC-R1 R1-3 scope (a); CL-R1-10 item 1).

Reads latitude and longitude only. Times and elevations are never read, so points without a time
are used as they are. Track points come first: every `trkpt` of every `trk`/`trkseg`, in file
order. Only when the file has no `trkpt` at all are the `rtept` of every `rte` used.

Privacy (CL-R1-10 item 7; SPEC-001 §2 privacy row): nothing here returns, raises or logs the path
or the file name. Errors carry a fixed reason code only; they never include the path, the file
name, a coordinate or the parser's own message, and they are raised without a chained exception.
This module does not log.

This reader is separate from `gpx.read_gpx` (the history GPX reader of Issue #9), which is not
changed.
"""
from __future__ import annotations

import hashlib
import math
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass

GPX_NAMESPACES = (
    "http://www.topografix.com/GPX/1/1",
    "http://www.topografix.com/GPX/1/0",
)

UNREADABLE = "unreadable"            # the file cannot be opened or is not a GPX document
MALFORMED_POINT = "malformed_point"  # a point has a missing, non-numeric or out-of-range lat/lon

# What `ET.fromstring` raises for bytes that cannot be decoded or parsed (audit issue-15-c1-r1,
# R1-F1). Only this one call is guarded, and only after `data` is known to be bytes:
# - ET.ParseError: not well-formed XML, undefined entities, the expat entity-expansion limit;
# - ValueError, including UnicodeError and UnicodeDecodeError: a declared multibyte or broken codec;
# - LookupError: a declared encoding that Python does not know, or a non-text codec (hex, zlib).
# Other exceptions (TypeError, AttributeError, MemoryError, RecursionError, ...) are not caught:
# they would be programming or resource errors, not content of the file.
_UNPARSEABLE = (ET.ParseError, ValueError, LookupError)


@dataclass(frozen=True)
class GeoPoint:
    """One point of the file: latitude and longitude in degrees, nothing else."""
    lat: float
    lon: float


@dataclass(frozen=True)
class GpxGeometry:
    """The points of a GPX file and the SHA-256 of the file's bytes.

    `source` is `"trkpt"` or `"rtept"` (`None` when the file has neither). There is no field for
    the path or the file name.
    """
    points: tuple[GeoPoint, ...]
    sha256: str
    source: str | None


class GpxGeometryError(ValueError):
    """The GPX cannot be read. `reason` is a fixed code; the message never names the file."""

    def __init__(self, reason: str):
        super().__init__(f"target GPX cannot be read ({reason})")
        self.reason = reason


def read_gpx_geometry(path: str | os.PathLike) -> GpxGeometry:
    """Read a GPX file from `path` (geometry only). The path is used to open the file and nothing else."""
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a str or an os.PathLike")  # an int would open a file descriptor
    data = None
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except (OSError, ValueError, TypeError):
        pass
    if data is None:
        # Raised outside the except block so that no OSError (which carries the file name) is
        # attached as the context of this error.
        raise GpxGeometryError(UNREADABLE)
    return parse_gpx_geometry(data)


def parse_gpx_geometry(data: bytes) -> GpxGeometry:
    """Parse GPX bytes (geometry only). `sha256` is the SHA-256 of exactly these bytes."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    data = bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    root = None
    try:
        root = ET.fromstring(data)
    except _UNPARSEABLE:
        pass
    if root is None:
        # Raised outside the except block: the parser's message and exception are not attached.
        raise GpxGeometryError(UNREADABLE)
    namespace = _gpx_namespace(root.tag)
    if namespace is None:
        raise GpxGeometryError(UNREADABLE)
    ns = {"g": namespace}
    nodes = root.findall("g:trk/g:trkseg/g:trkpt", ns)
    source = "trkpt"
    if not nodes:
        nodes = root.findall("g:rte/g:rtept", ns)
        source = "rtept"
    if not nodes:
        return GpxGeometry(points=(), sha256=digest, source=None)
    return GpxGeometry(points=tuple(_point(node) for node in nodes), sha256=digest, source=source)


def _gpx_namespace(tag: str) -> str | None:
    for namespace in GPX_NAMESPACES:
        if tag == f"{{{namespace}}}gpx":
            return namespace
    return None


def _point(node: ET.Element) -> GeoPoint:
    lat = _degrees(node.attrib.get("lat"), 90.0)
    lon = _degrees(node.attrib.get("lon"), 180.0)
    if lat is None or lon is None:
        raise GpxGeometryError(MALFORMED_POINT)
    return GeoPoint(lat, lon)


def _degrees(text: str | None, limit: float) -> float | None:
    if text is None:
        return None
    try:
        value = float(text.strip())
    except ValueError:
        return None
    if not math.isfinite(value) or abs(value) > limit:
        return None
    return value
