from classes import Route
import sys
from datetime import datetime

# temp imports
from preprocessing import preprocess
import cli_input

def dijkstra_time_factor_algorithm(routes: dict, start_stop: str, end_stop: str, start_time: datetime) -> dict:
    journey = {}
    
    # 'Q' set of graph nodes (stops)
    stops = create_stops_dictionary(routes, start_stop)
    
    #while stops (Q) not empty
    while stops:
        # delete stop with min value from stops
        mini_stop = stops.pop(find_min_dict_value(stops))
                
        
        
    
    return journey


def create_stops_dictionary(routes: dict, start_stop: str) -> dict:
    stops = {}
    for route in routes.values():
        stops[route.startStop.name] = sys.maxsize
        stops[route.endStop.name] = sys.maxsize
        
    stops[start_stop] = 0
    
    return stops

def find_min_dict_value(stops: dict) -> str:
    return min(stops, key=stops.get)

# find all neighbours of stop according to routes from this stop to neighbours after current time
def find_stop_neighbours(routes: dict, stops: dict, stop: str, time: datetime) -> dict:
    pass
    