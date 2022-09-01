from enum import Enum
from typing import Optional, Dict, List, Tuple, Iterable

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
    type: GeometryType = GeometryType.FEATURE
    properties: Optional[Dict[str, str]]
    geometry: Geometry


class FeatureCollection(BaseModel):
    type: GeometryType = GeometryType.FEATURE_COLLECTION
    features: List[Feature]

