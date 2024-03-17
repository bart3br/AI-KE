from classes import Route
from datetime import datetime, timedelta
import copy
# temp imports
from preprocessing import preprocess
import cli_input

# time in seconds needed to change to another line during journey
seconds_to_change = 60.0

def dijkstra_time_factor_algorithm(routes: dict, start_stop: str, end_stop: str, start_time: datetime) -> tuple:
    # set of all graph nodes (stops)
    # with key=stopName, value=tuple(cost (earliest known arrival time), route from parent)
    stops = create_stops_dictionary(routes, start_stop, start_time)
    
    # 'Q' set of graph nodes (stops) used for algorithm to choose current minimal cost nodes
    stops_queue = copy.deepcopy(stops)
    
    #while stops (Q) not empty
    while stops_queue:
        # find stop with min value from stops queue
        curr_stop = find_min_value_stop_key(stops_queue, start_time)
        find_and_update_stop_neighbours(routes, stops, stops_queue, curr_stop)
        # delete current stop from stops
        stops_queue.pop(curr_stop)
    
    # find optimal path and count total journey time            
    journey = find_optimal_path_in_stops(stops, end_stop)
    journey_total_time = count_optimal_journey_total_time(stops, start_time, end_stop)   
    return (journey, journey_total_time)

def create_stops_dictionary(routes: dict, start_stop: str, start_time: datetime) -> dict:
    stops = {}
    max_datetime = start_time.replace(year= start_time.year+1)
    for route in routes.values():
        stops[route.startStop.name] = (max_datetime, None)
        stops[route.endStop.name] = (max_datetime, None)
    
    stops[start_stop] = (start_time, None)
    return stops

def find_min_value_stop_key(stops: dict, start_time: datetime) -> str:
    earliest_key = None
    max_datetime = start_time.replace(year= start_time.year+2)
    earliest_datetime = max_datetime

    for key, value in stops.items():
        if value[0] < earliest_datetime:
            earliest_datetime = value[0]
            earliest_key = key

    return earliest_key

# find all neighbours of stop according to routes from this stop to neighbours after current time
# and update their arrival times (cost) and parents
def find_and_update_stop_neighbours(routes: dict, stops: dict, stops_queue: dict, curr_stop: str) -> None:
    for key, route in routes.items():
        # check if route's startStop is the current stop and if it's possible to change due to current time
        if (route.startStop.name == curr_stop and is_route_departure_time_valid(stops, route)):
            stops[route.endStop.name] = update_value_and_parent_for_stop(route, stops)
            if (route.endStop.name in stops_queue):
                stops_queue[route.endStop.name] = copy.copy(stops[route.endStop.name])


# checking if route departure time from current stop is not earlier than arrival to current stop
# and can be taken into consideration when updating optimal routes
def is_route_departure_time_valid(stops: dict, route: Route) -> bool:
    curr_stop = route.startStop.name
    curr_stop_arrival_time = (stops.get(curr_stop))[0]   
    return route.departureTime >= curr_stop_arrival_time

# counting new value to get from current to neighbour stop and assigning new parent if needed
def update_value_and_parent_for_stop(route: Route, stops: dict) -> tuple:
    curr_stop = route.startStop.name
    neighbour_stop = route.endStop.name
    
    curr_stop_tup = stops.get(curr_stop)
    neigbour_stop_tup = stops.get(neighbour_stop)

    curr_stop_arrival_time = curr_stop_tup[0] # d(u)
    neighbour_stop_arrival_time = neigbour_stop_tup[0] # d(v)

    curr_to_neighbour_cost = count_waiting_and_route_journey_time_cost(stops, route) # w(u,v)

    # if new cost is lower than previous, change parent to current route and update cost, else return unchanged values
    if (neighbour_stop_arrival_time > curr_stop_arrival_time + timedelta(seconds=curr_to_neighbour_cost)):
        return (route.arrivalTime, route)
    else:
        return neigbour_stop_tup

# returns time in seconds from arrival to current stop (current stop cost)
# to arrival to neighbour stop (waiting for route start time + route time)
def count_waiting_and_route_journey_time_cost(stops: dict, route: Route) -> float:
    curr_stop = route.startStop.name
    curr_stop_arrival_time: datetime = (stops.get(curr_stop))[0]
    return (route.arrivalTime - curr_stop_arrival_time).total_seconds()
    
    

# after getting through dijkstra algorithm find the optimal path from end stop to start stop
def find_optimal_path_in_stops(stops: dict, end_stop: str) -> list:
    path = []
    curr_stop = stops[end_stop]
    parent_route = curr_stop[1] # route from parent to current stop

    while parent_route is not None:
        path.append(parent_route)
        curr_stop = stops[parent_route.startStop.name]
        parent_route = curr_stop[1]
    
    return reversed(path)

# count optimal path's total journey time
def count_optimal_journey_total_time(stops: dict, start_time: datetime, end_stop: str) -> str:
    end_stop_arrival_time: datetime = stops.get(end_stop)[0]
    delta = end_stop_arrival_time - start_time
    
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} h, {minutes} min, {seconds} s"

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
    for route in solution[0]:
        print(route)
    print(f"Total journey time: {solution[1]}")