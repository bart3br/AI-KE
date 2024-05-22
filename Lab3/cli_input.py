PROMPT_WIDTH = 34
FIELDS = ['power', 'heating', 'start_button', 'display', 'lighting']

def single_user_input(field_name: str, 
                      positive_answer: str, 
                      negative_answer: str) -> tuple:
    prompt = f"Is the {field_name} {positive_answer}? (Y/N)"
    prompt = prompt.ljust(PROMPT_WIDTH)
    if (input(prompt) == 'Y'):
        status = positive_answer
    else:
        status = negative_answer
    # expected_status = input(f"Should the {field_name} be {positive_answer}? Y/N ")
    # if ((expected_status == 'Y' and status == 'off')
    #     or (expected_status == 'N' and status == 'on')):
    #     return (field_name, status)
    # return (None, None)
    return (field_name, status)
    
def user_input() -> dict:
    microwave_state = {}
    print("Welcome to the microwave troubleshooting assistant")
    for field in FIELDS:
        status = single_user_input(field, 'on', 'off')
        if (status[0] is not None):
            microwave_state[status[0]] = status[1]
    door_status = single_user_input('door', 'open', 'closed')
    if (door_status[0] is not None):
            microwave_state[door_status[0]] = door_status[1]
    print('')
    return microwave_state

def display_user_input(facts: dict):
    for key, value in facts.items():
        print(f"{key} with status {value}")

if __name__ == "__main__":
    pass