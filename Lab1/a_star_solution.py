from classes import Route, Stop
from datetime import datetime, timedelta
import copy
import constants
from math import acos, pi

def a_star_time_factor_algorithm(stops_graph: dict, start_stop: str, end_stop: str, start_time: datetime, avg_speed: float) -> tuple:
    # set of all graph nodes (stops)
    # with key=stopName, value=tuple(cost (earliest known arrival time + heuristic), route from parent)
    stops = create_stops_dictionary(stops_graph, start_stop, start_time)
    
    # 'Q' set of graph nodes (stops) used for algorithm to choose current minimal cost nodes
    stops_queue = copy.deepcopy(stops)
    
    #while stops (Q) not empty
    while stops_queue:
        # find stop with min value from stops queue
        curr_stop = find_min_value_stop_key(stops_queue, start_time)
        #if current stop is end stop, then optimal path has been found, end algorithm
        if (curr_stop == end_stop):
            return finish_search(stops, end_stop, start_time)
        
        find_and_update_stop_neighbours(stops_graph, stops, stops_queue, curr_stop, start_time, end_stop, avg_speed)
        # delete current stop from stops
        stops_queue.pop(curr_stop)
                
    return finish_search(stops, end_stop, start_time)


# def a_star_line_change_factor_algorithm(stops_graph: dict, start_stop: str, end_stop: str, start_time: datetime) -> tuple:
#     avg_speed = count_avg_speed_of_all_routes(stops_graph)
#     # set of all graph nodes (stops)
#     # with key=stopName, value=tuple(cost (number of line changes + heuristic), route from parent)
#     stops = create_stops_dictionary(stops_graph, start_stop, start_time)
    
#     # 'Q' set of graph nodes (stops) used for algorithm to choose current minimal cost nodes
#     stops_queue = copy.deepcopy(stops)
    
#     #while stops (Q) not empty
#     while stops_queue:
#         # find stop with min value from stops queue
#         curr_stop = find_min_value_stop_key(stops_queue, start_time)
#         #if current stop is end stop, then optimal path has been found, end algorithm
#         if (curr_stop == end_stop):
#             return finish_search(stops, end_stop, start_time)
        
#         find_and_update_stop_neighbours(stops_graph, stops, stops_queue, curr_stop, start_time, end_stop)
#         # delete current stop from stops
#         stops_queue.pop(curr_stop)
                
#     return finish_search(stops, end_stop, start_time)



# find optimal path and count total journey time
def finish_search(stops, end_stop, start_time):
    journey = find_optimal_path_in_stops(stops, end_stop)
    journey_total_time = count_optimal_journey_total_time(stops, start_time, end_stop)   
    return (journey, journey_total_time)

# create stops dictionary to store arrival times and routes to parents stops
def create_stops_dictionary(stops_graph: dict, start_stop: str, start_time: datetime) -> dict:
    stops = {}
    max_datetime = start_time.replace(year= start_time.year+1)
    for stop_name in stops_graph.keys():
        stops[stop_name] = (max_datetime, None)
    
    stops[start_stop] = (start_time, None)
    return stops

# find candidate for next current stop
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
def find_and_update_stop_neighbours(stops_graph: dict, stops: dict, stops_queue: dict, curr_stop: str, start_time: datetime, end_stop: str, avg_speed: float) -> None:
    connections_dict: dict = stops_graph.get(curr_stop)
    for routes_list in connections_dict.values():
        earliest_valid_route_indx = find_earliest_valid_route_indx(stops, routes_list, start_time)
        if (earliest_valid_route_indx != -1):
            earliest_valid_route = routes_list[earliest_valid_route_indx]
            stops[earliest_valid_route.endStop.name] = update_value_and_parent_for_stop(stops_graph, earliest_valid_route, stops, end_stop, avg_speed)
            if (earliest_valid_route.endStop.name in stops_queue):
                stops_queue[earliest_valid_route.endStop.name] = copy.copy(stops[earliest_valid_route.endStop.name])


# find earliest route from routes_list (all routes from current stop to one neighbour)
# route's departure time must be after current stop arrival time + possible time needed for line change
def find_earliest_valid_route_indx(stops: dict, routes_list: list, start_time: datetime) -> int:
    earliest_key = -1
    earliest_datetime = start_time.replace(year= start_time.year+2)
    for indx, route in enumerate(routes_list):
        if (earliest_datetime > route.departureTime and is_route_departure_time_valid(stops, route, start_time)):
            earliest_key = indx
            earliest_datetime = route.departureTime
    return earliest_key



# checking if route departure time from current stop is not earlier than arrival to current stop
# and can be taken into consideration when updating optimal routes
def is_route_departure_time_valid(stops: dict, route: Route, start_time: datetime) -> bool:
    curr_stop = route.startStop.name
    route_to_curr_stop: Route = (stops.get(curr_stop))[1]
    curr_stop_arrival_time = start_time
    if (route_to_curr_stop is not None):
        curr_stop_arrival_time = route_to_curr_stop.arrivalTime

    return route.departureTime >= curr_stop_arrival_time + timedelta(seconds=check_and_count_line_change_cost(stops, route))

# counting new value to get from current to neighbour stop and assigning new parent if needed
def update_value_and_parent_for_stop(stops_graph: dict, route: Route, stops: dict, end_stop: str, avg_speed: float) -> tuple:
    curr_stop = route.startStop.name
    neighbour_stop = route.endStop.name
    
    curr_stop_tup = stops.get(curr_stop)
    neigbour_stop_tup = stops.get(neighbour_stop)

    curr_stop_arrival_time = curr_stop_tup[0] # d(u)
    neighbour_stop_arrival_time = neigbour_stop_tup[0] # d(v)

    curr_to_neighbour_cost = count_waiting_and_route_journey_time_cost(stops_graph, stops, route, end_stop, avg_speed) # w(u,v) + HEURISTIC
    new_arrival_time_cost = curr_stop_arrival_time + timedelta(seconds=curr_to_neighbour_cost)

    # if new cost is lower than previous, change parent to current route and update cost, else return unchanged values
    if (neighbour_stop_arrival_time > new_arrival_time_cost):
        return (new_arrival_time_cost, route)
    else:
        return neigbour_stop_tup

# returns time in seconds from arrival to current stop (current stop cost)
# to arrival to neighbour stop + HEURISTIC (waiting for route start time + route time + heuristic func value)
def count_waiting_and_route_journey_time_cost(stops_graph: dict, stops: dict, route: Route, end_stop: str, avg_speed: float) -> float:
    curr_stop = route.startStop.name
    curr_stop_arrival_time: datetime = (stops.get(curr_stop))[0]
    waiting_and_journey_cost = (route.arrivalTime - curr_stop_arrival_time).total_seconds()
    return waiting_and_journey_cost + count_heuristic_in_seconds(stops_graph, route, end_stop, avg_speed)

def count_heuristic_in_seconds(stops_graph: dict, route: Route, end_stop: str, avg_speed: float) -> float:
    curr_stop = route.startStop.name
    neighbour_stop = route.endStop.name

    curr_neighbour_random_route = ((stops_graph[curr_stop]).get(neighbour_stop))[0]
    end_any_random_route = (next(iter((stops_graph[end_stop]).values())))[0]
    
    
    curr_stop_obj = curr_neighbour_random_route.startStop
    neighbour_stop_obj = curr_neighbour_random_route.endStop
    end_stop_obj = end_any_random_route.startStop

    angle = count_angle_between_stops(curr_stop_obj, neighbour_stop_obj, end_stop_obj) # [0, 180]
    dist_neighbour_end = neighbour_stop_obj.euclidean_dist(end_stop_obj)
    estimated_time_neighbour_end = dist_neighbour_end / avg_speed
    return (angle / 180.0) * estimated_time_neighbour_end


def count_angle_between_stops(curr_stop_obj: Stop, neighbour_stop_obj: Stop, end_stop_obj: Stop) -> float:
    dist_curr_neighbour = curr_stop_obj.euclidean_dist(neighbour_stop_obj) # dist_b
    dist_curr_end = curr_stop_obj.euclidean_dist(end_stop_obj) # dist_a
    dist_neighbour_end = neighbour_stop_obj.euclidean_dist(end_stop_obj) # dist_c

    angle_in_radians =  count_acb_angle_using_law_of_cosines(dist_curr_end, dist_curr_neighbour, dist_neighbour_end)
    return angle_in_radians * (180.0 / pi)

# count angle by C vertex in ABC triangle, where dist_a = BC, dist_b = AC, dist_c = AB
def count_acb_angle_using_law_of_cosines(dist_a: float, dist_b: float, dist_c: float) -> float:
    if (dist_a + dist_b == dist_c):
        return acos(-1.0) # 180 degrees
    if (dist_a + dist_c == dist_b or dist_b + dist_c == dist_a):
        return acos(1.0) # 0 degrees
    return acos((pow(dist_a, 2) + pow(dist_b, 2) - pow(dist_c, 2)) / (2.0 * dist_a * dist_b))


# check if there is about to be line change
# and return the cost of change if line change happens
def check_and_count_line_change_cost(stops: dict, route: Route) -> float:
    curr_stop = route.startStop.name
    route_to_curr_stop: Route = (stops.get(curr_stop))[1]
    if route_to_curr_stop is None or route_to_curr_stop.line == route.line:
        return 0.0 # there is no line change
    return constants.COST_OF_THE_LINE_CHANGE # there is line change


# after getting through a-star algorithm find the optimal path from end stop to start stop
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
    pass