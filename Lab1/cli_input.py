import time
from classes import Route

def cli_load_data(filename: str, event) -> None:
    print("Loading data from " + filename + "...")
    timer = 0
    while not event.is_set():
        print(f"Loading... ({timer}s)")
        timer += 5
        time.sleep(5)
        
def cli_user_input() -> tuple:
    print("\nData loaded successfully.")
    print("Data contains timetable of Wrocław's public transport on March 01, 2023.")
    print(" - Enter start destination: ")
    start = input()
    print(" - Enter end destination: ")
    end = input()
    print(" - Enter route finding decision factor\n   t - quickest route\n   p - min number of changes: ")
    factor = input()
    print(" - Enter journey start time (hh:mm:ss): ")
    start_time = input()
    
    return (start, end, factor, start_time)


def validate_user_input(routes: dict, input: tuple) -> bool:
    #start_stop = next((stop for stop.startStop.name in routes.values()), None)
    pass

def cli_output_route(route: Route) -> None:
    print(route.__str__())
    
def cli_output_total_time(time: str) -> None:
    pass

def cli_output_cost_fun_value(value: str) -> None:
    pass

if __name__ == "__main__":
    pass
    