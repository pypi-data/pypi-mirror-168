from datetime import datetime


class Stop():
    
    def __init__(self, data: dict):

        self.name = data["name"]
        self.id = data["id"]
        if "extId" in data:
            self.ext_id = data["extId"]
        else:
            self.ext_id = None
        self.lon = data["lon"]
        self.lat = data["lat"]

    def __str__(self) -> str:
        return f"Stop {self.name} at {self.lon}, {self.lat}"

class StopTrip(Stop):

    def __init__(self, data: dict):
        
        self.type = data["type"]
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        self.time = datetime.strptime(data["time"], "%H:%M:%S")
        super().__init__(data)

    def __str__(self) -> str:
        return f"Stop {self.name} at {self.lon}, {self.lat} at {self.time.time()} {self.date.date()}"