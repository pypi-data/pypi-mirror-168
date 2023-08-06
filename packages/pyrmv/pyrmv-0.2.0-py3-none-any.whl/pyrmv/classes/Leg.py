from pyrmv.classes.Gis import Gis
from pyrmv.classes.Stop import StopTrip
from isodate import parse_duration

class Leg():
    def __init__(self, data: dict):
        self.origin = StopTrip(data["Origin"])
        self.destination = StopTrip(data["Destination"])
        if "GisRef" in data:
            self.gis = Gis(data["GisRef"]["ref"], data["GisRoute"])
        else:
            self.gis = None
        self.index = data["idx"]
        self.name = data["name"]
        self.type = data["type"]
        self.duration = parse_duration(data["duration"])
        if "dist" in data:
            self.distance = data["dist"]
        else:
            self.distance = None