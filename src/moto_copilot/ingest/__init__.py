"""GPX ingestion (Pre-Spec Technical Spike, M1-A): GPX -> Derived Segment Table."""
from .gpx import read_gpx
from .segments import (
    IngestParams,
    TrackPoint,
    TripReport,
    build_rows,
    category_of,
    curvature_deg_per_km,
    haversine_m,
    moving_path,
    to_public,
)

__all__ = [
    "IngestParams",
    "TrackPoint",
    "TripReport",
    "build_rows",
    "category_of",
    "curvature_deg_per_km",
    "haversine_m",
    "moving_path",
    "read_gpx",
    "to_public",
]
