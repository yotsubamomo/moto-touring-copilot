"""CR-01 routing checks: one throttled, disk-cached client for the public Valhalla server and Nominatim.

Rules built in (the owner's conditions for the public services):
  * only public landmarks may be sent; this module never reads a GPX file
  * at most one request per MIN_INTERVAL_S seconds over both hosts, also across script runs
  * every response (errors included) is cached on disk; an identical request is never sent twice
  * hard caps on the number of requests; a refusal or rate limit writes a STOP file and nothing
    more is sent until a person removes it
  * a generic User-Agent; no name, email or project name in any request

Everything is written under data/private/cr01/ (git-ignored).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "data" / "private" / "cr01"
CACHE = PRIVATE / "http_cache"
LOG = PRIVATE / "routing_request_log.jsonl"
STOP = PRIVATE / "routing_STOP"
LAST = PRIVATE / "routing_last_request.txt"

USER_AGENT = "route-snapshot-check/0.1 (course project; low volume)"
VALHALLA = "https://valhalla1.openstreetmap.de"
NOMINATIM = "https://nominatim.openstreetmap.org/search"
MIN_INTERVAL_S = 1.6
CAPS = {"routing": 55, "geocoding": 38}
TAIPEI = dt.timezone(dt.timedelta(hours=8))


class Stopped(RuntimeError):
    """The server refused or rate-limited a request, or a cap was reached. Nothing more is sent."""


def counts() -> dict[str, int]:
    out = {"routing": 0, "geocoding": 0}
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            out[json.loads(line)["kind"]] += 1
    return out


def _send(kind: str, key_material: str, request: urllib.request.Request, describe: dict) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(key_material.encode("utf-8")).hexdigest()
    cached = CACHE / f"{key}.json"
    if cached.exists():
        return json.loads(cached.read_text(encoding="utf-8"))
    if STOP.exists():
        raise Stopped(f"STOP file present: {STOP.read_text(encoding='utf-8').strip()}")
    if counts()[kind] >= CAPS[kind]:
        raise Stopped(f"request cap reached for {kind}")
    if LAST.exists():
        wait = MIN_INTERVAL_S - (time.time() - float(LAST.read_text()))
        if wait > 0:
            time.sleep(wait)
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            status, body = response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        status, body = error.code, error.read().decode("utf-8", errors="replace")
    finally:
        LAST.write_text(str(time.time()))
    now = dt.datetime.now(TAIPEI).isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as log:
        log.write(json.dumps({"kind": kind, "at": now, "status": status, "key": key, **describe}, ensure_ascii=False) + "\n")
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        parsed = {"_raw": body[:2000]}
    record = {"kind": kind, "fetched_at": now, "status": status, "request": describe, "body": parsed}
    if status in (403, 429) or status >= 500:
        STOP.write_text(f"{now} {kind} HTTP {status}", encoding="utf-8")
        (CACHE / f"{key}.refused.json").write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        raise Stopped(f"{kind} request answered HTTP {status}; stopped")
    cached.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
    return record


def valhalla(action: str, body: dict) -> dict:
    """POST one request to the public Valhalla server. Returns {status, body, fetched_at, request}."""
    payload = json.dumps(body, sort_keys=True, ensure_ascii=False)
    request = urllib.request.Request(f"{VALHALLA}/{action}", data=payload.encode("utf-8"), method="POST",
                                     headers={"Content-Type": "application/json", "User-Agent": USER_AGENT})
    return _send("routing", f"valhalla|{action}|{payload}", request, {"action": action, "body": body})


def geocode(query: str) -> dict:
    """Free-text search for one public landmark name in Taiwan."""
    params = {"q": query, "format": "jsonv2", "limit": 5, "countrycodes": "tw", "accept-language": "zh-TW"}
    url = f"{NOMINATIM}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return _send("geocoding", f"nominatim|{url}", request, {"action": "search", "query": query})


def decode6(shape: str) -> list[tuple[float, float]]:
    """Valhalla encoded polyline, six decimal places -> [(lat, lon)]."""
    out, i, lat, lon = [], 0, 0, 0
    while i < len(shape):
        for k in range(2):
            shift = result = 0
            while True:
                b = ord(shape[i]) - 63
                i += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            delta = ~(result >> 1) if result & 1 else result >> 1
            if k == 0:
                lat += delta
            else:
                lon += delta
        out.append((lat / 1e6, lon / 1e6))
    return out


def route_body(locations: list[dict], *, exclude_highways: bool = True, elevation_interval: float | None = 30.0) -> dict:
    """The one request shape used for every snapshot: motorcycle costing, national freeways excluded."""
    body = {"locations": [{"lat": round(p["lat"], 6), "lon": round(p["lon"], 6), "type": "break"} for p in locations],
            "costing": "motorcycle", "units": "kilometers"}
    if exclude_highways:
        body["costing_options"] = {"motorcycle": {"exclude_highways": True}}
    if elevation_interval:
        body["elevation_interval"] = elevation_interval
    return body
