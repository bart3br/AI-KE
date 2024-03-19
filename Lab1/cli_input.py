import time
from classes import Route
from datetime import datetime
import constants

def cli_load_data(filename: str, increment: int, event) -> None:
    print("Loading data from " + filename + "...")
    timer = 0
    while not event.is_set():
        print(f"Loading... ({timer}s)")
        timer += increment
        time.sleep(increment)
        
def cli_user_input() -> tuple:
    print("\nData loaded successfully.")
    print("Data contains timetable of Wrocław's public transport on March 01, 2023.")
    # print(" - Enter start destination: ")
    start = input(" - Enter start destination: ")
    # print(" - Enter end destination: ")
    end = input(" - Enter end destination: ")
    # print(" - Enter route finding decision factor\n   t - quickest route\n   p - min number of changes: ")
    factor = input(" - Enter route finding decision factor\n   t - quickest route\n   p - min number of changes: ")
    # print(" - Enter journey start time (hh:mm:ss): ")
    start_time = input(" - Enter journey start time (hh:mm:ss): ")
    
    return (start, end, factor, start_time)


def validate_user_input(stops_graph: dict, input_tup: tuple) -> bool:
    start, end, factor, start_time = input_tup
    validate = True
    if (start not in stops_graph.keys()):
        print("Start destination doesn't exist.")
        validate = False
    if (end not in stops_graph.keys()):
        print("End destination doesn't exist.")
        validate = False
    if (factor not in ['t', 'p']):
        print("Wrong decision factor choice.")
        validate = False
    if (not validate_start_time_format(start_time)):
        print("Wrong journey start time format.")
        validate = False
    
    return validate

def validate_start_time_format(start_time: str) -> bool:
    try:
        datetime.strptime(start_time, constants.TIME_FORMAT)
        return True
    except ValueError:
        return False
    
def create_start_time_datetime(start_hour: str) -> datetime:
    day_datetime = datetime.strptime(constants.DATE, constants.DATE_FORMAT)
    hour_datetime = datetime.strptime(start_hour, constants.TIME_FORMAT).time()
    return datetime.combine(day_datetime, hour_datetime)


def cli_output_route(route: Route) -> None:
    print(route.__str__())
    
def cli_output_total_time(time: str) -> None:
    pass

def cli_output_cost_fun_value(value: str) -> None:
    pass

if __name__ == "__main__":
    pass
    