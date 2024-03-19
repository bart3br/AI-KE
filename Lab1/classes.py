import math
from datetime import datetime

# instance of a Stop class represents one Stop with defined name, lattitude and longtitude
class Stop:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        
    def __str__(self):
        return f"{self.name} at {self.lat}, {self.lon}"
    
    # this approximation can be used due to all the coordinates being north-east
    # and the points being within the same mid-sized city, so the Earth curvature doesn't matter
    def euclidean_dist(self, other: 'Stop'):
        return math.sqrt(math.pow(self.lat - other.lat, 2) + math.pow(self.lon - other.lon, 2))


# instance of Route class represents one row of data
class Route:
    def __init__(self, **kwargs):
        self.company: str = kwargs["company"]
        self.line: str = kwargs["line"]
        self.departureTime: datetime = kwargs["departure_time"]
        self.arrivalTime: datetime = kwargs["arrival_time"]
        self.startStop = Stop(kwargs["start_stop"], kwargs["start_stop_lat"], kwargs["start_stop_lon"])
        self.endStop = Stop(kwargs["end_stop"], kwargs["end_stop_lat"], kwargs["end_stop_lon"])
        
    def __str__(self):
        return f"Line {self.line}, from {self.startStop.name} at {self.departureTime}, to {self.endStop.name} at {self.arrivalTime}"
    
    def journey_time_seconds(self) -> float:
        return abs((self.arrivalTime - self.departureTime).total_seconds())
    
    


if __name__ == "__main__":
    pass
