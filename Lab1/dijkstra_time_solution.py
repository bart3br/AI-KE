from classes import Route
import sys
from datetime import datetime, time
import copy

# temp imports
from preprocessing import preprocess
import cli_input

# time in seconds needed to change to another line during journey
seconds_to_change = 60.0

def dijkstra_time_factor_algorithm(routes: dict, start_stop: str, end_stop: str, start_time: datetime) -> list:
    curr_time = copy.copy(start_time)
    
    # 'Q' set of graph nodes (stops) with key=stopName, value=tuple(cost, route from parent)
    stops = create_stops_dictionary(routes, start_stop)
    stops_queue = copy.deepcopy(stops)
    # set of visited nodes (stops) with key=stopName, value=tuple(cost, route from parent)
    visited_stops = {}

    # temp = stops[start_stop]
    # print(f"{temp[0]} and {temp[1].__str__()}")
    
    #while stops (Q) not empty
    while stops_queue:
        # find stop with min value from stops
        curr_stop = find_min_value_stop_key(stops_queue)

        # if current stop has a parent route, take it's arrivalTime as current time
        if (stops_queue[curr_stop][1] is not None):
            curr_time = (stops_queue[curr_stop][1]).arrivalTime
        print(curr_time)

        find_and_update_stop_neighbours(routes, stops, stops_queue, curr_stop, curr_time)
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
def find_and_update_stop_neighbours(routes: dict, stops: dict, stops_queue: dict, curr_stop: str, curr_time: datetime) -> None:
    for key, route in routes.items():
        # check if route's startStop is the current stop and if it's possible to change due to current time
        if (route.startStop.name == curr_stop and is_route_departure_time_not_too_late(route, curr_time)):
            stops[route.endStop.name] = update_value_and_parent_for_stop(route, stops, curr_stop, route.endStop.name)
            if (route.endStop.name in stops_queue):
                stops_queue[route.endStop.name] = stops[route.endStop.name]


def is_route_departure_time_not_too_late(route: Route, time: datetime) -> bool:
    time_delta = (route.departureTime - time).total_seconds()
    return time_delta >= 0.0

# counting new value to get from current to neighbour stop and assigning new parent if needed
def update_value_and_parent_for_stop(route: Route, stops: dict, curr_stop: str, neighbour_stop: str) -> tuple:
    curr_stop_tup = stops.get(curr_stop)
    # if (neighbour_stop in stops):
    #     print("neighbour exists, ", neighbour_stop)
    # else:
    #     print("neighbour DOESNT exist, ", neighbour_stop)
    neigbour_stop_tup = stops.get(neighbour_stop)

    # if (neighbour_stop == "Kwiska"):
    #     print("WRACA NA KWISKA")

    # if neigbour_stop_tup is None:
    #     print(f"TU SIE WYPIERDALA: current_stop = {curr_stop}, neighbour_stop = {neighbour_stop}")
    #     print(f"route = {route.__str__()}, current_stop_tuple = ({curr_stop_tup[0]}, {curr_stop_tup[1].__str__()}")

    # if (neighbour_stop == "Kwiska"):
    #     return (float('inf'), None)

    curr_stop_value = curr_stop_tup[0] # d(u)
    neighbour_stop_value = neigbour_stop_tup[0] # d(v)
    curr_to_neighbour_value = route.journey_time_seconds() # w(u,v)

    # if new value is lower than previous, change parent to current node and update value, else return unchanged values
    new_value = curr_stop_value + curr_to_neighbour_value
    if (neighbour_stop_value > new_value):
        return (new_value, route)
    else:
        return neigbour_stop_tup

# after getting through dijkstra algorithm find the optimal path from end stop to start stop
def find_optimal_path_in_visited_stops(visited_stops: dict, start_stop: str, end_stop: str) -> list:
    path = []
    curr_stop = visited_stops[end_stop]
    parent_route = curr_stop[1] # route from parent to current stop
    # print(curr_stop[1].__str__())

    while parent_route is not None:
        path.append(parent_route)
        curr_stop = visited_stops[parent_route.startStop.name]
        parent_route = curr_stop[1]
        # print(curr_stop[1].__str__())
    
    return reversed(path)

if __name__ == "__main__":
    routes = preprocess()
    input = cli_input.cli_user_input()

    date = "01.03.2023"
    date_format = "%d.%m.%Y"
    time_format = "%H:%M:%S"
    day_datetime = datetime.strptime(date, date_format)
    date_str = "10:05:00"
    time_datetime = datetime.strptime(date_str, time_format).time()

    time_temp = datetime.combine(day_datetime, time_datetime)
    print(time_temp)

    # for key, route in routes.items():
    #     if (route.line == "3"):
    #         if (route.endStop.name == "DH Astra"):
    #             print(route.__str__())
    #for key, route in routes.items():


    solution = dijkstra_time_factor_algorithm(routes, input[0], input[1], time_temp)
    for route in solution:
        print(route)
    