# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = osr_itineraire_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast
from datetime import datetime


T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()





@dataclass
class Geometry:
    coordinates: List[List[float]]
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Geometry':
        assert isinstance(obj, dict)
        coordinates = from_list(lambda x: from_list(from_float, x), obj.get("coordinates"))
        type = from_str(obj.get("type"))
        return Geometry(coordinates, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordinates"] = from_list(lambda x: from_list(to_float, x), self.coordinates)
        result["type"] = from_str(self.type)
        return result


@dataclass
class Step:
    distance: float
    duration: float
    type: int
    instruction: str
    name: str
    way_points: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'Step':
        assert isinstance(obj, dict)
        distance = from_float(obj.get("distance"))
        duration = from_float(obj.get("duration"))
        type = from_int(obj.get("type"))
        instruction = from_str(obj.get("instruction"))
        name = from_str(obj.get("name"))
        way_points = from_list(from_int, obj.get("way_points"))
        return Step(distance, duration, type, instruction, name, way_points)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distance"] = to_float(self.distance)
        result["duration"] = to_float(self.duration)
        result["type"] = from_int(self.type)
        result["instruction"] = from_str(self.instruction)
        result["name"] = from_str(self.name)
        result["way_points"] = from_list(from_int, self.way_points)
        return result


@dataclass
class Segment:
    distance: float
    duration: float
    steps: List[Step]

    @staticmethod
    def from_dict(obj: Any) -> 'Segment':
        assert isinstance(obj, dict)
        distance = from_float(obj.get("distance"))
        duration = from_float(obj.get("duration"))
        steps = from_list(Step.from_dict, obj.get("steps"))
        return Segment(distance, duration, steps)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distance"] = to_float(self.distance)
        result["duration"] = to_float(self.duration)
        result["steps"] = from_list(lambda x: to_class(Step, x), self.steps)
        return result


@dataclass
class Summary:
    distance: float
    duration: float

    @staticmethod
    def from_dict(obj: Any) -> 'Summary':
        assert isinstance(obj, dict)
        distance = from_float(obj.get("distance"))
        duration = from_float(obj.get("duration"))
        return Summary(distance, duration)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distance"] = to_float(self.distance)
        result["duration"] = to_float(self.duration)
        return result


@dataclass
class Properties:
    segments: List[Segment]
    summary: Summary
    way_points: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'Properties':
        assert isinstance(obj, dict)
        segments = from_list(Segment.from_dict, obj.get("segments"))
        summary = Summary.from_dict(obj.get("summary"))
        way_points = from_list(from_int, obj.get("way_points"))
        return Properties(segments, summary, way_points)

    def to_dict(self) -> dict:
        result: dict = {}
        result["segments"] = from_list(lambda x: to_class(Segment, x), self.segments)
        result["summary"] = to_class(Summary, self.summary)
        result["way_points"] = from_list(from_int, self.way_points)
        return result


@dataclass
class Feature:
    bbox: List[float]
    type: str
    properties: Properties
    geometry: Geometry

    @staticmethod
    def from_dict(obj: Any) -> 'Feature':
        assert isinstance(obj, dict)
        bbox = from_list(from_float, obj.get("bbox"))
        type = from_str(obj.get("type"))
        properties = Properties.from_dict(obj.get("properties"))
        geometry = Geometry.from_dict(obj.get("geometry"))
        return Feature(bbox, type, properties, geometry)

    def to_dict(self) -> dict:
        result: dict = {}
        result["bbox"] = from_list(to_float, self.bbox)
        result["type"] = from_str(self.type)
        result["properties"] = to_class(Properties, self.properties)
        result["geometry"] = to_class(Geometry, self.geometry)
        return result



@dataclass
class Query:
    coordinates: List[List[float]]
    profile: str
    format: str

    @staticmethod
    def from_dict(obj: Any) -> 'Query':
        assert isinstance(obj, dict)
        coordinates = from_list(lambda x: from_list(from_float, x), obj.get("coordinates"))
        profile = from_str(obj.get("profile"))
        format = from_str(obj.get("format"))
        return Query(coordinates, profile, format)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordinates"] = from_list(lambda x: from_list(to_float, x), self.coordinates)
        result["profile"] = from_str(self.profile)
        result["format"] = from_str(self.format)
        return result


@dataclass
class Metadata:
    attribution: str
    service: str
    timestamp: int
    query: Query

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        assert isinstance(obj, dict)
        attribution = from_str(obj.get("attribution"))
        service = from_str(obj.get("service"))
        timestamp = from_int(obj.get("timestamp"))
        query = Query.from_dict(obj.get("query"))
        return Metadata(attribution, service, timestamp, query)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attribution"] = from_str(self.attribution)
        result["service"] = from_str(self.service)
        result["timestamp"] = from_int(self.timestamp)
        result["query"] = to_class(Query, self.query)
        return result


@dataclass
class OsrItineraire:
    type: str
    features: List[Feature]
    bbox: List[float]
    metadata: Metadata

    @staticmethod
    def from_dict(obj: Any) -> 'OsrItineraire':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        features = from_list(Feature.from_dict, obj.get("features"))
        bbox = from_list(from_float, obj.get("bbox"))
        metadata = Metadata.from_dict(obj.get("metadata"))
        return OsrItineraire(type, features, bbox, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["features"] = from_list(lambda x: to_class(Feature, x), self.features)
        result["bbox"] = from_list(to_float, self.bbox)
        result["metadata"] = to_class(Metadata, self.metadata)
        return result


def osr_itineraire_from_dict(s: Any) -> OsrItineraire:
    return OsrItineraire.from_dict(s)


def osr_itineraire_to_dict(x: OsrItineraire) -> Any:
    return to_class(OsrItineraire, x)
