from enum import Enum
from typing import Dict, List, Tuple, Any

from pydantic import BaseModel


class GeometryType(str, Enum):
    POINT = "Point",
    MULTI_POINT = "MultiPoint",
    LINE_STRING = "LineString",
    MULTI_LINE_STRING = "MultiLineString",
    POLYGON = "Polygon",
    MULTI_POLYGON = "MultiPolygon",
    GEOMETRY_COLLECTION = "GeometryCollection",
    FEATURE = "Feature"
    FEATURE_COLLECTION = "FeatureCollection"


class Geometry(BaseModel):
    type: GeometryType
    coordinates: List[float] | List[List[float]]


class PointGeometry(Geometry):
    type: GeometryType = GeometryType.POINT
    coordinates: Tuple[float, float]


class Feature(BaseModel):
    id: str | None
    type: GeometryType = GeometryType.FEATURE
    bbox: List[float] | None
    properties: Dict[str, Any] | None
    geometry: Geometry


class FeatureCollection(BaseModel):
    type: GeometryType = GeometryType.FEATURE_COLLECTION
    bbox: List[float] | None
    features: List[Feature]
