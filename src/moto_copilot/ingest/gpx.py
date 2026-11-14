"""Read track points from a GPX 1.1 file exported by BMW Motorrad Connected."""
from __future__ import annotations

import datetime as dt
import xml.etree.ElementTree as ET
from pathlib import Path

from .segments import TrackPoint

_NS = {"g": "http://www.topografix.com/GPX/1/1"}


def read_gpx(path: Path) -> tuple[list[TrackPoint], int]:
    """Return the points that carry a time, in file order, and the number of points without one.

    GPX times are UTC ("...Z"); they are kept timezone-aware and converted to +08:00 on output.
    """
    points: list[TrackPoint] = []
    without_time = 0
    for node in ET.parse(path).getroot().iterfind(".//g:trkpt", _NS):
        time_node = node.find("g:time", _NS)
        if time_node is None or not time_node.text:
            without_time += 1
            continue
        stamp = dt.datetime.fromisoformat(time_node.text.strip().replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=dt.timezone.utc)
        points.append(TrackPoint(float(node.attrib["lat"]), float(node.attrib["lon"]), stamp))
    return points, without_time
