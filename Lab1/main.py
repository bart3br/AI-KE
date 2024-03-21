import threading
from queue import Queue
from datetime import datetime
import time

from preprocessing import preprocess
import cli_input
from dijkstra_time_solution import dijkstra_time_factor_algorithm
from a_star_time_solution import a_star_time_factor_algorithm
from a_star_line_change_solution import a_star_line_change_factor_algorithm
import constants

def load_data() -> tuple:
    load_data_queue = Queue()
    event = threading.Event()
    data_loading_thread = threading.Thread(target=preprocess, args=(load_data_queue, event,))
    loading_message_thread = threading.Thread(target=cli_input.cli_load_data, args=(constants.FILENAME, 10, event,))
    
    data_loading_thread.start()
    loading_message_thread.start()
    
    data_loading_thread.join()

    stops_graph = load_data_queue.get()
    avg_speed = load_data_queue.get()
    
    loading_message_thread.join()
    return (stops_graph, avg_speed)


def run_dijkstra(stops_graph: dict, start_stop: str, end_stop: str, start_time: datetime) -> None:
    print("\nDijkstra algorithm with time factor solution")
    time1 = time.time()
    solution = dijkstra_time_factor_algorithm(stops_graph, start_stop, end_stop, start_time)
    time2 = time.time()
    print_journey_info(solution[0], solution[1], time1, time2)

def run_a_star_time(stops_graph: dict, start_stop: str, end_stop: str, start_time: datetime, avg_speed: float) -> None:
    print("\nA* algorithm with time factor solution")
    time1 = time.time()
    solution = a_star_time_factor_algorithm(stops_graph, start_stop, end_stop, start_time, avg_speed)
    time2 = time.time()
    print_journey_info(solution[0], solution[1], time1, time2)

def run_a_star_line_change(stops_graph: dict, start_stop: str, end_stop: str, start_time: datetime) -> None:
    print("\nA* algorithm with line change factor solution")
    time1 = time.time()
    solution = a_star_line_change_factor_algorithm(stops_graph, start_stop, end_stop, start_time)
    time2 = time.time()
    print_journey_info(solution[0], solution[1], time1, time2)


def print_journey_info(route_list: list, total_journey_time: str, time1: float, time2: float) -> None:
    route_list = list(route_list)
    prev = None
    curr = None
    line_change_counter = 0
    for i, route in enumerate(route_list):
        prev = curr
        curr = route
        if (prev is None):
            print(curr.str_first_half(), end="")
        elif (prev.line != curr.line or prev.arrivalTime != curr.departureTime):
            print(prev.str_second_half())
            print(curr.str_first_half(), end="")
            line_change_counter += 1
        if (i == len(route_list) - 1):
            print(curr.str_second_half())
    print(f"Total journey time: {total_journey_time}")
    print(f"Number of line changes: {line_change_counter}")
    print(f"Route calculation time: {int((time2 - time1) * 1000)} ms")


def run_main() -> None:
    stops_graph, avg_speed = load_data()
    
    run = True
    while run:
        input_tup = cli_input.cli_user_input(stops_graph)
        start_stop, end_stop, factor, start_time = input_tup
        start_time = cli_input.create_start_time_datetime(start_time)
        
        perform_calculations = True
        while perform_calculations:
            action_choice = cli_input.cli_action_choice_input(factor)
            match (action_choice, factor):
                case (0, _):
                    perform_calculations = False
                    run = False
                case (1, 't'):
                    run_dijkstra(stops_graph, start_stop, end_stop, start_time)
                case (1, 'p'):
                    run_a_star_line_change(stops_graph, start_stop, end_stop, start_time)
                case (2, 't'):
                    run_a_star_time(stops_graph, start_stop, end_stop, start_time, avg_speed)
                case (2, 'p') | (3, 't'):
                    perform_calculations = False
                case (4, 't'):
                    factor = 'p'
                case (3, 'p'):
                    factor = 't'

if __name__ == "__main__":
    run_main()