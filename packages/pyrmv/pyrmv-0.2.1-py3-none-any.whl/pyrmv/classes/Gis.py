from isodate import parse_duration

class Gis():
    
    def __init__(self, ref: str, route: dict):
        
        self.ref = ref
        self.dist = route["dist"]
        self.duration = parse_duration(route["durS"])
        self.geo = route["dirGeo"]