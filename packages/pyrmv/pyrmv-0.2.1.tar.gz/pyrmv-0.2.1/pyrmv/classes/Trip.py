from pyrmv.classes.Leg import Leg
from pyrmv.classes.Stop import StopTrip
from isodate import parse_duration

class Trip():
    
    def __init__(self, data: dict):
        
        self.raw_data = data
        self.origin = StopTrip(data["Origin"])
        self.destination = StopTrip(data["Destination"])

        self.legs = []
        for leg in data["LegList"]["Leg"]:
            self.legs.append(Leg(leg))

        self.calculation = data["calculation"]
        self.index = data["idx"]
        self.id = data["tripId"]
        self.ctx_recon = data["ctxRecon"]
        self.duration = parse_duration(data["duration"])

        if "rtDuration" in data:
            self.real_time_duration = parse_duration(data["rtDuration"])
        else:
            self.real_time_duration = None

        self.checksum = data["checksum"]
        
        if "transferCount" in data:
            self.transfer_count = data["transferCount"]
        else:
            self.transfer_count = 0

    def __str__(self) -> str:
        return f"Trip from {self.origin.name} to {self.destination.name} lasting {self.duration} ({self.real_time_duration}) with {len(self.legs)} legs and {self.transfer_count} transfers"