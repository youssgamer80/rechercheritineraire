# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = mapbox_itineraire_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


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
class Admin:
    iso_3166_1__alpha3: str
    iso_3166_1: str

    @staticmethod
    def from_dict(obj: Any) -> 'Admin':
        assert isinstance(obj, dict)
        iso_3166_1__alpha3 = from_str(obj.get("iso_3166_1_alpha3"))
        iso_3166_1 = from_str(obj.get("iso_3166_1"))
        return Admin(iso_3166_1__alpha3, iso_3166_1)

    def to_dict(self) -> dict:
        result: dict = {}
        result["iso_3166_1_alpha3"] = from_str(self.iso_3166_1__alpha3)
        result["iso_3166_1"] = from_str(self.iso_3166_1)
        return result


@dataclass
class Leg:
    via_waypoints: List[Any]
    admins: List[Admin]
    weight: float
    duration: float
    steps: List[Any]
    distance: float
    summary: str

    @staticmethod
    def from_dict(obj: Any) -> 'Leg':
        assert isinstance(obj, dict)
        via_waypoints = from_list(lambda x: x, obj.get("via_waypoints"))
        admins = from_list(Admin.from_dict, obj.get("admins"))
        weight = from_float(obj.get("weight"))
        duration = from_float(obj.get("duration"))
        steps = from_list(lambda x: x, obj.get("steps"))
        distance = from_float(obj.get("distance"))
        summary = from_str(obj.get("summary"))
        return Leg(via_waypoints, admins, weight, duration, steps, distance, summary)

    def to_dict(self) -> dict:
        result: dict = {}
        result["via_waypoints"] = from_list(lambda x: x, self.via_waypoints)
        result["admins"] = from_list(lambda x: to_class(Admin, x), self.admins)
        result["weight"] = to_float(self.weight)
        result["duration"] = to_float(self.duration)
        result["steps"] = from_list(lambda x: x, self.steps)
        result["distance"] = to_float(self.distance)
        result["summary"] = from_str(self.summary)
        return result


@dataclass
class Route:
    country_crossed: bool
    weight_name: str
    weight: float
    duration: float
    distance: float
    legs: List[Leg]
    geometry: Geometry

    @staticmethod
    def from_dict(obj: Any) -> 'Route':
        assert isinstance(obj, dict)
        country_crossed = from_bool(obj.get("country_crossed"))
        weight_name = from_str(obj.get("weight_name"))
        weight = from_float(obj.get("weight"))
        duration = from_float(obj.get("duration"))
        distance = from_float(obj.get("distance"))
        legs = from_list(Leg.from_dict, obj.get("legs"))
        geometry = Geometry.from_dict(obj.get("geometry"))
        return Route(country_crossed, weight_name, weight, duration, distance, legs, geometry)

    def to_dict(self) -> dict:
        result: dict = {}
        result["country_crossed"] = from_bool(self.country_crossed)
        result["weight_name"] = from_str(self.weight_name)
        result["weight"] = to_float(self.weight)
        result["duration"] = to_float(self.duration)
        result["distance"] = to_float(self.distance)
        result["legs"] = from_list(lambda x: to_class(Leg, x), self.legs)
        result["geometry"] = to_class(Geometry, self.geometry)
        return result


@dataclass
class Waypoint:
    distance: float
    name: str
    location: List[float]

    @staticmethod
    def from_dict(obj: Any) -> 'Waypoint':
        assert isinstance(obj, dict)
        distance = from_float(obj.get("distance"))
        name = from_str(obj.get("name"))
        location = from_list(from_float, obj.get("location"))
        return Waypoint(distance, name, location)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distance"] = to_float(self.distance)
        result["name"] = from_str(self.name)
        result["location"] = from_list(to_float, self.location)
        return result


@dataclass
class MapboxItineraire:
    routes: List[Route]
    waypoints: List[Waypoint]
    code: str
    uuid: str

    @staticmethod
    def from_dict(obj: Any) -> 'MapboxItineraire':
        assert isinstance(obj, dict)
        routes = from_list(Route.from_dict, obj.get("routes"))
        waypoints = from_list(Waypoint.from_dict, obj.get("waypoints"))
        code = from_str(obj.get("code"))
        uuid = from_str(obj.get("uuid"))
        return MapboxItineraire(routes, waypoints, code, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["routes"] = from_list(lambda x: to_class(Route, x), self.routes)
        result["waypoints"] = from_list(lambda x: to_class(Waypoint, x), self.waypoints)
        result["code"] = from_str(self.code)
        result["uuid"] = from_str(self.uuid)
        return result


def mapbox_itineraire_from_dict(s: Any) -> MapboxItineraire:
    return MapboxItineraire.from_dict(s)


def mapbox_itineraire_to_dict(x: MapboxItineraire) -> Any:
    return to_class(MapboxItineraire, x)