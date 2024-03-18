import pandas as pd
from datetime import datetime
from classes import Route
from copy import copy

filename = "connection_graph.csv"
col_types = {
    'id':int,
    'company': str,
    'line': str,
    'departure_time': str,
    'arrival_time': str,
    'start_stop': str,
    'end_stop': str,
    'start_stop_lat': float,
    'start_stop_lon': float,
    'end_stop_lat': float,
    'end_stop_lon': float
}

# data from connection_graph.csv file refers to 1st of March 2023
date = "01.03.2023"
date_format = "%d.%m.%Y"
time_format = "%H:%M:%S"


def read_data():
    data = pd.read_csv(filename, dtype=col_types)
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
    time_tup = fix_time_after_midnight(copy(date), hour_str)
    
    day_datetime = datetime.strptime(time_tup[0], date_format)
    hour_datetime = datetime.strptime(time_tup[1], time_format).time()
    
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

# def create_stops_graph(routes: dict) -> dict:
#     stops_graph = {}
#     for route in routes.values():
#         stops_graph[route.startStop.name] = {}
#         stops_graph[route.endStop.name] = {}
    
    
#     return 

def preprocess(result_queue, event):
    data = read_data()
    dictionary = dataframe_to_route_dict(data)
    result_queue.put(dictionary)
    event.set()
    # return dictionary
    


if __name__ == "__main__":
    pass