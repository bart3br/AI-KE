import cli_input

def run():
    game_state = cli_input.read_initial_game_state()
    cli_input.cli_print_initial_game_state(game_state)

if __name__ == "__main__":
    run()
