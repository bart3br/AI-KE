from cli_input import user_input, display_user_input
from facts_and_rules import MicrowaveExpertSystem, ProblemFact

def diagnose_microwave_issues(facts: dict):
    system = MicrowaveExpertSystem()
    system.reset()
    for field, status in facts.items():
        system.declare(ProblemFact(**{field: status}))
    system.run()
    

if __name__ == "__main__":
    microwave_status = user_input()
    # display_user_input(microwave_status)
    diagnose_microwave_issues(microwave_status)