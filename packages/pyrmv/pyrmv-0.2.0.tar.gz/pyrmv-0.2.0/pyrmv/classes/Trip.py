from pyrmv.classes.Leg import Leg
from pyrmv.classes.Stop import StopTrip
from isodate import parse_duration

class Trip():
    
    def __init__(self, data: dict):
        self.raw_data = data
        self.origin = StopTrip(data["Origin"])
        self.destination = StopTrip(data["Destination"])
        legs = []
        for leg in data["LegList"]["Leg"]:
            legs.append(Leg(leg))
        self.legs = legs
        self.calculation = data["calculation"]
        self.index = data["idx"]
        self.id = data["tripId"]
        self.ctx_recon = data["ctxRecon"]
        self.duration = parse_duration(data["duration"])
        self.real_time_duration = parse_duration(data["rtDuration"])
        self.checksum = data["checksum"]
        self.transfer_count = data["transferCount"]

    def __str__(self) -> str:
        return f"Trip from {self.origin.name} to {self.destination.name} lasting {self.duration} ({self.real_time_duration}) with {len(self.legs)} legs and {self.transfer_count} transfers"