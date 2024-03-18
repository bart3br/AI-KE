from preprocessing import preprocess
import cli_input
import threading
from queue import Queue
from datetime import datetime
from dijkstra_time_solution import dijkstra_time_factor_algorithm
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
    
    loading_message_thread.join()
    
    input = cli_input.cli_user_input() 
    day_datetime = datetime.strptime(constants.DATE, constants.DATE_FORMAT)
    hour_datetime = datetime.strptime(input[3], constants.TIME_FORMAT).time()
    start_time = datetime.combine(day_datetime, hour_datetime)
    print(f"Journey start time was set to {start_time}")

    # solution = dijkstra_time_factor_algorithm(routes, input[0], input[1], start_time)
    solution = dijkstra_time_factor_algorithm(stops_graph, input[0], input[1], start_time)
    for route in solution[0]:
        print(route)
    print(f"Total journey time: {solution[1]}")