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
        
def cli_user_input(stops_graph: dict) -> tuple:
    validate_input = False
    input_tup = ()
    while (not validate_input):
        input_tup = get_user_input()
        validate_input = validate_user_input(stops_graph, input_tup)
    return input_tup

def cli_action_choice_input(factor: int) -> int:
    validate_input = False
    action_choice = 0
    while not validate_input:
        action_choice = choose_option_or_exit_program(factor)
        validate_input = validate_option_choice(action_choice, factor)
    return int(action_choice)
        
def get_user_input() -> tuple:
    print("\nData loaded successfully.")
    print("Data contains timetable of Wrocław's public transport on March 01, 2023.")
    start = input(" - Enter start destination: ")
    end = input(" - Enter end destination: ")
    factor = input(" - Enter route finding decision factor\n   t - quickest route\n   p - min number of changes: ")
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

def choose_option_or_exit_program(factor: str) -> str:
    print("\nChoose action to perform:")
    if (factor == 't'):
        print("   1 - Calculate best route with Dijkstra (time factor) algorithm")
        print("   2 - Calculate best route with A* (time factor) algorithm")
        print("   3 - Change journey information (start/end stop, factor, start time)")
        print("   4 - Switch decision factor (current: t)")
        print("   0 - Exit program")
    else:
        print("   1 - Calculate best route with A* (line change factor) algorithm")
        print("   2 - Change journey information (start/end stop, factor, start time)")
        print("   3 - Switch decision factor (current: p)")
        print("   0 - Exit program")
    choice = input("Your choice: ")
    return choice
        
def validate_option_choice(user_choice: str, factor: str) -> bool:
    if (factor == 't'):
        try:
            user_choice_num = int(user_choice)
            return user_choice_num in [0,1,2,3,4]
        except ValueError or TypeError:
            return False
    else:
        try:
            user_choice_num = int(user_choice)
            return user_choice_num in [0,1,2,3]
        except ValueError or TypeError:
            return False

def cli_output_route(route: Route) -> None:
    print(route.__str__())
    
def cli_output_total_time(time: str) -> None:
    pass

def cli_output_cost_fun_value(value: str) -> None:
    pass

if __name__ == "__main__":
    pass
    