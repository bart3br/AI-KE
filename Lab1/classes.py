import math
import datetime

# instance of a Stop class represents one Stop with defined name, lattitude and longtitude
class Stop:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        
    def __str__(self):
        return f"{self.name} at {self.lat}, {self.lon}"
    
    def EuclideanDist(self, other: 'Stop'):
        return math.sqrt(math.pow(self.lat - other.lat, 2) + math.pow(self.lon - other.lon, 2))


# instance of Route class represents one row of data
class Route:
    def __init__(self, **kwargs):
        self.company = kwargs["company"]
        self.line = kwargs["line"]
        self.departureTime = kwargs["departure_time"]
        self.arrivalTime = kwargs["arrival_time"]
        self.startStop = Stop(kwargs["start_stop"], kwargs["start_stop_lat"], kwargs["start_stop_lon"])
        self.endStop = Stop(kwargs["end_stop"], kwargs["end_stop_lat"], kwargs["end_stop_lon"])
        
    def __str__(self):
        return f"Line {self.line}, from {self.startStop.name} to {self.endStop.name}"


if __name__ == "__main__":
    pass
