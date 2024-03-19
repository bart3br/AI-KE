import threading
from queue import Queue
from datetime import datetime
import time

from preprocessing import preprocess
import cli_input
from dijkstra_time_solution import dijkstra_time_factor_algorithm
from a_star_solution import a_star_time_factor_algorithm
import constants

if __name__ == "__main__":
    load_data_queue = Queue()
    event = threading.Event()
    data_loading_thread = threading.Thread(target=preprocess, args=(load_data_queue, event,))
    loading_message_thread = threading.Thread(target=cli_input.cli_load_data, args=("connection_graph.csv", 10, event,))
    
    data_loading_thread.start()
    loading_message_thread.start()
    
    data_loading_thread.join()

    # routes = load_data_queue.get()
    stops_graph = load_data_queue.get()
    avg_speed = load_data_queue.get()
    
    loading_message_thread.join()
    
    validate_input = False
    input_tup = ()
    while (not validate_input):
        input_tup = cli_input.cli_user_input()
        validate_input = cli_input.validate_user_input(stops_graph, input_tup)

    start_time = cli_input.create_start_time_datetime(input_tup[3])
    print(f"Journey start time was set to {start_time}")

    print("\nDijkstra algorithm with time factor solution")
    time1 = time.time()
    solution = dijkstra_time_factor_algorithm(stops_graph, input_tup[0], input_tup[1], start_time)
    time2 = time.time()
    for route in solution[0]:
        print(route)
    print(f"Total journey time: {solution[1]}")
    print(f"Route calculation time: {int((time2 - time1) * 1000)} ms")

    print("\nA* algorithm with time factor solution")
    time1 = time.time()
    solution = a_star_time_factor_algorithm(stops_graph, input_tup[0], input_tup[1], start_time, avg_speed)
    time2 = time.time()
    for route in solution[0]:
        print(route)
    print(f"Total journey time: {solution[1]}")
    print(f"Route calculation time: {int((time2 - time1) * 1000)} ms")