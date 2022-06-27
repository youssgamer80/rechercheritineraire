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
#     result = osr_matrix_duration_from_dict(json.loads(json_string))

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


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x





def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Destination:
    location: List[float]
    snapped_distance: float

    @staticmethod
    def from_dict(obj: Any) -> 'Destination':
        assert isinstance(obj, dict)
        location = from_list(from_float, obj.get("location"))
        snapped_distance = from_float(obj.get("snapped_distance"))
        return Destination(location, snapped_distance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["location"] = from_list(to_float, self.location)
        result["snapped_distance"] = to_float(self.snapped_distance)
        return result





@dataclass
class Query:
    locations: List[List[float]]
    profile: str
    response_type: str
    metrics_strings: List[str]
    metrics: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Query':
        assert isinstance(obj, dict)
        locations = from_list(lambda x: from_list(from_float, x), obj.get("locations"))
        profile = from_str(obj.get("profile"))
        response_type = from_str(obj.get("responseType"))
        metrics_strings = from_list(from_str, obj.get("metricsStrings"))
        metrics = from_list(from_str, obj.get("metrics"))
        return Query(locations, profile, response_type, metrics_strings, metrics)

    def to_dict(self) -> dict:
        result: dict = {}
        result["locations"] = from_list(lambda x: from_list(to_float, x), self.locations)
        result["profile"] = from_str(self.profile)
        result["responseType"] = from_str(self.response_type)
        result["metricsStrings"] = from_list(from_str, self.metrics_strings)
        result["metrics"] = from_list(from_str, self.metrics)
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
class OsrMatrixDuration:
    distances: List[List[float]]
    destinations: List[Destination]
    sources: List[Destination]
    metadata: Metadata

    @staticmethod
    def from_dict(obj: Any) -> 'OsrMatrixDuration':
        assert isinstance(obj, dict)
        distances = from_list(lambda x: from_list(from_float, x), obj.get("distances"))
        destinations = from_list(Destination.from_dict, obj.get("destinations"))
        sources = from_list(Destination.from_dict, obj.get("sources"))
        metadata = Metadata.from_dict(obj.get("metadata"))
        return OsrMatrixDuration(distances, destinations, sources, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distances"] = from_list(lambda x: from_list(to_float, x), self.distances)
        result["destinations"] = from_list(lambda x: to_class(Destination, x), self.destinations)
        result["sources"] = from_list(lambda x: to_class(Destination, x), self.sources)
        result["metadata"] = to_class(Metadata, self.metadata)
        return result


def osr_matrix_duration_from_dict(s: Any) -> OsrMatrixDuration:
    return OsrMatrixDuration.from_dict(s)


def osr_matrix_duration_to_dict(x: OsrMatrixDuration) -> Any:
    return to_class(OsrMatrixDuration, x)
