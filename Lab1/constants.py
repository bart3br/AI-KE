# data filename
FILENAME = "connection_graph.csv"

# data from connection_graph.csv file refers to 1st of March 2023
DATE = "01.03.2023"
DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M:%S"

SECONDS_IN_ONE_DAY = 86400.0

# column types for pandas to read data from .csv file properly
COL_TYPES = {
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

# time in seconds needed to change to another line during journey
COST_OF_THE_LINE_CHANGE = 30.0