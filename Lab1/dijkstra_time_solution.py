from classes import Route
import sys
from datetime import datetime, time, timedelta
import copy

# temp imports
from preprocessing import preprocess
import cli_input

# time in seconds needed to change to another line during journey
seconds_to_change = 60.0

def dijkstra_time_factor_algorithm(routes: dict, start_stop: str, end_stop: str, start_time: datetime) -> list:
    # set of all graph nodes (stops) with key=stopName, value=tuple(cost, route from parent)
    stops = create_stops_dictionary(routes, start_stop)
    
    # 'Q' set of graph nodes (stops) used for algorithm to choose current minimal cost nodes
    stops_queue = copy.deepcopy(stops)
    
    # set of visited nodes (stops)
    visited_stops = {}
    
    #while stops (Q) not empty
    while stops_queue:
        # find stop with min value from stops queue
        curr_stop = find_min_value_stop_key(stops_queue)
        find_and_update_stop_neighbours(routes, stops, stops_queue, curr_stop, start_time)
        # add current stop to visited stops
        visited_stops[curr_stop] = stops_queue.get(curr_stop)
        # delete current stop from stops
        stops_queue.pop(curr_stop)
                
    journey = find_optimal_path_in_visited_stops(visited_stops, start_stop, end_stop)   
    return journey


def create_stops_dictionary(routes: dict, start_stop: str) -> dict:
    stops = {}
    for route in routes.values():
        stops[route.startStop.name] = (float('inf'), None)
        stops[route.endStop.name] = (float('inf'), None)
    
    stops[start_stop] = (0.0, None)
    return stops

def find_min_value_stop_key(stops: dict) -> str:
    return min(stops, key=lambda k: stops[k][0])

# find all neighbours of stop according to routes from this stop to neighbours after current time
# and update their values (cost) and parents
def find_and_update_stop_neighbours(routes: dict, stops: dict, stops_queue: dict, curr_stop: str, start_time: datetime) -> None:
    for key, route in routes.items():
        # check if route's startStop is the current stop and if it's possible to change due to current time
        if (route.startStop.name == curr_stop and is_route_departure_time_valid(stops, curr_stop, route, start_time)):
            stops[route.endStop.name] = update_value_and_parent_for_stop(route, stops, start_time)
            if (route.endStop.name in stops_queue):
                stops_queue[route.endStop.name] = copy.copy(stops[route.endStop.name])


# checking if route departure time from current stop is not earlier than arrival to current stop
# and can be taken into consideration when updating optimal routes
def is_route_departure_time_valid(stops: dict, curr_stop: str, route: Route, start_time: datetime) -> bool:
    curr_stop_cost_seconds = (stops.get(curr_stop))[0]
    # TODO
    if (curr_stop_cost_seconds == float('inf')):
        return False
    curr_stop_arrival_time = start_time + timedelta(seconds=curr_stop_cost_seconds)
    return route.departureTime >= curr_stop_arrival_time

# TODO not working properly, traveling back in time
# counting new value to get from current to neighbour stop and assigning new parent if needed
def update_value_and_parent_for_stop(route: Route, stops: dict, start_time: datetime) -> tuple:
    curr_stop = route.startStop.name
    neighbour_stop = route.endStop.name
    
    curr_stop_tup = stops.get(curr_stop)
    neigbour_stop_tup = stops.get(neighbour_stop)

    curr_stop_arrival_cost = curr_stop_tup[0] # d(u)
    neighbour_stop_arrival_cost = neigbour_stop_tup[0] # d(v)

    curr_to_neighbour_cost = count_waiting_and_route_journey_time_cost(route, stops, start_time) # w(u,v)

    # if new cost is lower than previous, change parent to current route and update cost, else return unchanged values
    if (neighbour_stop_arrival_cost > curr_stop_arrival_cost + curr_to_neighbour_cost):
        return (curr_to_neighbour_cost, route)
    else:
        return neigbour_stop_tup

# returns time in seconds from arrival to current stop (current stop cost)
# to arrival to neighbour stop (waiting for route start time + route time)
def count_waiting_and_route_journey_time_cost(route: Route, stops: dict, start_time: datetime) -> float:
    curr_stop = route.startStop.name
    curr_stop_cost_seconds = (stops.get(curr_stop))[0]
    
    curr_time = start_time + timedelta(seconds=curr_stop_cost_seconds)
    return (route.arrivalTime - curr_time).total_seconds()

# after getting through dijkstra algorithm find the optimal path from end stop to start stop
def find_optimal_path_in_visited_stops(visited_stops: dict, start_stop: str, end_stop: str) -> list:
    path = []
    curr_stop = visited_stops[end_stop]
    parent_route = curr_stop[1] # route from parent to current stop

    while parent_route is not None:
        path.append(parent_route)
        curr_stop = visited_stops[parent_route.startStop.name]
        parent_route = curr_stop[1]
    
    return reversed(path)

if __name__ == "__main__":
    routes = preprocess()
    input = cli_input.cli_user_input()

    date = "01.03.2023"
    date_format = "%d.%m.%Y"
    time_format = "%H:%M:%S"
    
    day_datetime = datetime.strptime(date, date_format)
    hour_datetime = datetime.strptime(input[3], time_format).time()

    start_time = datetime.combine(day_datetime, hour_datetime)
    print(start_time)

    solution = dijkstra_time_factor_algorithm(routes, input[0], input[1], start_time)
    for route in solution:
        print(route)
    