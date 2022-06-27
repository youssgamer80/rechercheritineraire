# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = trafffic_duration_from_dict(json.loads(json_string))

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


class Destination:
    distance: float
    name: str
    location: List[float]

    def __init__(self, distance: float, name: str, location: List[float]) -> None:
        self.distance = distance
        self.name = name
        self.location = location

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


class TraffficDuration:
    code: str
    durations: List[List[float]]
    destinations: List[Destination]
    sources: List[Destination]

    def __init__(self, code: str, durations: List[List[float]], destinations: List[Destination], sources: List[Destination]) -> None:
        self.code = code
        self.durations = durations
        self.destinations = destinations
        self.sources = sources

    @staticmethod
    def from_dict(obj: Any) -> 'TraffficDuration':
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        durations = from_list(lambda x: from_list(from_float, x), obj.get("durations"))
        destinations = from_list(Destination.from_dict, obj.get("destinations"))
        sources = from_list(Destination.from_dict, obj.get("sources"))
        return TraffficDuration(code, durations, destinations, sources)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        result["durations"] = from_list(lambda x: from_list(to_float, x), self.durations)
        result["destinations"] = from_list(lambda x: to_class(Destination, x), self.destinations)
        result["sources"] = from_list(lambda x: to_class(Destination, x), self.sources)
        return result


def trafffic_duration_from_dict(s: Any) -> TraffficDuration:
    return TraffficDuration.from_dict(s)


def trafffic_duration_to_dict(x: TraffficDuration) -> Any:
    return to_class(TraffficDuration, x)
