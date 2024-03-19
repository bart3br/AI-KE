import pandas as pd
from datetime import datetime
from classes import Route, Stop
from copy import copy
import constants

def read_data():
    data = pd.read_csv(constants.FILENAME, dtype=constants.COL_TYPES)
    #add missing id column name
    data.rename(columns={data.columns[0]: "id"}, inplace=True)
    return data

#fix night courses times after midnight having >24h format
def fix_time_after_midnight(day_str: str, hour_str: str):
    hour = int(hour_str[:2])
    if (hour >= 24):
        hour -= 24
        hour_str = str(hour) + hour_str[2:]
        day_str = day_str.replace(day_str[1], str(int(day_str[1])+1), 1)
    return (day_str, hour_str)

def date_str_to_datetime(hour_str: str):
    time_tup = fix_time_after_midnight(copy(constants.DATE), hour_str)
    
    day_datetime = datetime.strptime(time_tup[0], constants.DATE_FORMAT)
    hour_datetime = datetime.strptime(time_tup[1], constants.TIME_FORMAT).time()
    
    day_hour_datetime = datetime.combine(day_datetime, hour_datetime)
    return day_hour_datetime


def data_row_to_route_tuple(row) -> tuple:
    route = Route(
        company=row["company"], 
        line=row["line"], 
        departure_time=date_str_to_datetime(row["departure_time"]),
        arrival_time=date_str_to_datetime(row["arrival_time"]),
        start_stop=row["start_stop"],
        start_stop_lat=row["start_stop_lat"],
        start_stop_lon=row["start_stop_lon"],
        end_stop=row["end_stop"],
        end_stop_lat=row["end_stop_lat"],
        end_stop_lon=row["end_stop_lon"]
    )
    return (row["id"], route)

def dataframe_to_route_dict(data: pd.DataFrame) -> dict:
    dictionary = {}
    
    for index, row in data.iterrows():
        tup = data_row_to_route_tuple(row)
        dictionary[tup[0]] = tup[1]
    
    return dictionary

# dictionary with (key= stop_name, value= dict(key= neighbour_stop_name, value= list_of_routes from stop_name to neighbour))
def create_stops_graph(routes: dict) -> dict:
    stops_graph = {}
    for route in routes.values():
        add_route_to_stops_graph(stops_graph, route)

    return stops_graph

def add_route_to_stops_graph(stops_graph: dict, route: Route) -> None:
    curr_stop = route.startStop.name
    neighbour_stop = route.endStop.name
    if curr_stop in stops_graph:
        connections: dict = stops_graph[curr_stop]
        if neighbour_stop in connections:
            connections[neighbour_stop].append(route)
        else:
            connections[neighbour_stop] = [route]
    else:
        stops_graph[curr_stop] = {neighbour_stop: [route]}


# count average speed of all vehicles considering every route
# unit = degrees / days
def count_avg_speed_of_all_routes(routes: dict) -> float:
    total_distance = 0.0
    total_time = 0.0
    for route in routes.values():
        curr_stop_obj: Stop = route.startStop
        neighbour_stop_obj: Stop = route.endStop
        total_distance += curr_stop_obj.euclidean_dist(neighbour_stop_obj)
        total_time += route.journey_time_seconds()
    total_time = total_time / constants.SECONDS_IN_ONE_DAY
    return total_distance / total_time

def preprocess(result_queue, event):
    data = read_data()
    routes = dataframe_to_route_dict(data)
    stops_graph = create_stops_graph(routes)
    avg_speed = count_avg_speed_of_all_routes(routes)

    # result_queue.put(routes)
    result_queue.put(stops_graph)
    result_queue.put(avg_speed)
    event.set()
    


if __name__ == "__main__":
    pass