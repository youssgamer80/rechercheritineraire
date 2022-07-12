# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = mapbox_matrice_distance_duration_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Destination:
    distance: float
    name: str
    location: List[float]

    @staticmethod
    def from_dict(obj: Any) -> 'Destination':
        assert isinstance(obj, dict)
        distance = from_float(obj.get("distance"))
        name = from_str(obj.get("name"))
        location = from_list(from_float, obj.get("location"))
        return Destination(distance, name, location)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distance"] = to_float(self.distance)
        result["name"] = from_str(self.name)
        result["location"] = from_list(to_float, self.location)
        return result


@dataclass
class MapboxMatriceDistanceDuration:
    code: str
    distances: List[List[float]]
    durations: List[List[float]]
    destinations: List[Destination]
    sources: List[Destination]

    @staticmethod
    def from_dict(obj: Any) -> 'MapboxMatriceDistanceDuration':
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        distances = from_list(lambda x: from_list(from_float, x), obj.get("distances"))
        durations = from_list(lambda x: from_list(from_float, x), obj.get("durations"))
        destinations = from_list(Destination.from_dict, obj.get("destinations"))
        sources = from_list(Destination.from_dict, obj.get("sources"))
        return MapboxMatriceDistanceDuration(code, distances, durations, destinations, sources)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        result["distances"] = from_list(lambda x: from_list(to_float, x), self.distances)
        result["durations"] = from_list(lambda x: from_list(to_float, x), self.durations)
        result["destinations"] = from_list(lambda x: to_class(Destination, x), self.destinations)
        result["sources"] = from_list(lambda x: to_class(Destination, x), self.sources)
        return result


def mapbox_matrice_distance_duration_from_dict(s: Any) -> MapboxMatriceDistanceDuration:
    return MapboxMatriceDistanceDuration.from_dict(s)


def mapbox_matrice_distance_duration_to_dict(x: MapboxMatriceDistanceDuration) -> Any:
    return to_class(MapboxMatriceDistanceDuration, x)
