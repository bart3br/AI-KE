import pandas as pd
from datetime import datetime
from classes import Route

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
    data = pd.read_csv("connection_graph.csv", dtype=col_types)
    #add missing id column name
    data.rename(columns={data.columns[0]: "id"}, inplace=True)
    return data

#fix night courses times after midnight having >24h format
def fix_time_after_midnight(date_str: str):
    hour = int(date_str[:2])
    if (hour >= 24):
        hour -= 24
        date_str = str(hour) + date_str[2:]
    return date_str

def date_str_to_datetime(date_str: str):
    day_datetime = datetime.strptime(date, date_format)
    
    date_str = fix_time_after_midnight(date_str)
    time_datetime = datetime.strptime(date_str, time_format).time()
    
    day_time_datetime = datetime.combine(day_datetime, time_datetime)
    return day_time_datetime


def data_row_to_route_tuple(row):
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

def preprocess(data: pd.DataFrame) -> dict:
    dictionary = {}
    
    for index, row in data.iterrows():
        tup = data_row_to_route_tuple(row)
        dictionary[tup[0]] = tup[1]
    
    return dictionary

def temp():
    data = read_data()
    dictionary = preprocess(data)
    for key, value in dictionary.items():
        print (key, value)
    


if __name__ == "__main__":
    data = pd.read_csv('connection_graph.csv', dtype=col_types)
    print(data.head(10))
    temp()