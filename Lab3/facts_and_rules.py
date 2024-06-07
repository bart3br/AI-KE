from experta import Fact, KnowledgeEngine, Rule, Field, NOT, OR, AND

class ProblemFact(Fact):
    """provides information about microwave state,
       used by expert system to check the rules conditions"""
    pass
    

class MicrowaveExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.messages = {}
        
    def add_message(self, component: str, message: str):
        if component not in self.messages:
            self.messages[component] = []
        if (message not in self.messages[component]):
            self.messages[component].append(message)
    
    # no power rules
    @Rule(ProblemFact(power= "off"))
    def no_power_solution(self):
        self.declare(ProblemFact(description= "power off"))
        self.add_message('power',
                         "Check if the power cable is connected to the power plug")
    
    # no heating rules   
    @Rule(NOT(ProblemFact(description= "power off")),
          ProblemFact(heating= "off"))
    def no_heating_problem(self):
        self.declare(ProblemFact(description= "heating off"))
      
    @Rule(ProblemFact(description= "heating off"),
          ProblemFact(door= "open"))
    def no_heating_open_door_solution(self):
        self.declare(ProblemFact(description= "door open"))
        self.add_message('heating',
                         "Close the microwave door before turning heating on")
        
    @Rule(ProblemFact(description= "heating off"),
          NOT(ProblemFact(description= "door open")),
          ProblemFact(start_button= "off"))
    def no_heating_closed_door_solution(self):
        self.declare(ProblemFact(description= "start button not clicked"))
        self.add_message('heating',
                         "Set the desired heating time and click start button to start the heating")
        
    @Rule(ProblemFact(description= "heating off"),
          NOT(ProblemFact(description= "door open")),
          ProblemFact(start_button= "on"))
    def no_heating_closed_door_start_on_solution(self):
        self.declare(ProblemFact(description= "heating broken"))
        self.add_message('heating', 
                         "Try unplugging and pluging the power cable back to the power plug")
        self.add_message('heating', 
                         "If the microwave still doesn't turn on the heating, contact authorized service center")
    
    # display off rules 
    @Rule(ProblemFact(power= "on"),
          ProblemFact(display= "off"))
    def display_off_power_on_solution(self):
        self.declare(ProblemFact(description= "display off"))
        self.add_message('display', 
                         "Try unplugging and pluging the power cable back to the power plug")
        self.add_message('display',
                         "If the display is still off, contact authorized service center")
    
    # lighting off rules
    @Rule(ProblemFact(power= "on"),
          ProblemFact(lighting= "off"))
    def lighting_off_problem(self):
        self.declare(ProblemFact(description= "lighting off"))
        
    @Rule(ProblemFact(description= "lighting off"),
          ProblemFact(description="heating off"),
          ProblemFact(door= "closed"))
    def lighting_off_solution(self):
        self.declare(ProblemFact(description= "lighting off door closed"))
        self.add_message('lighting',
                         "Open the door or start heating process to trigger the lighting on")
        
    @Rule(ProblemFact(description="lighting off"),
          OR(ProblemFact(door= "open"), ProblemFact(heating= "on")))
    def lighting_off_broken_solution(self):
        self.declare(ProblemFact(description= "lighting off broken"))
        self.add_message('lighting',
                         "Lighting is not working, the bulb needs replacing")
        self.add_message('lighting',
                         "Contact authorized service center to change the bulb")
        
    # device malfunction rules
    @Rule(NOT(ProblemFact(description= "power off")),
          ProblemFact(heating= "on"),
          ProblemFact(start_button= "off"))
    def start_button_malfunction_solution(self):
        self.declare(ProblemFact(description= "start_button broken"))
        self.add_message('start_button',
                         "Start button is malfunctioning, contact authorized service center")
        
    @Rule(NOT(ProblemFact(description= "power off")),
          ProblemFact(heating= "on"),
          ProblemFact(door= "open"))
    def heating_door_malfunction_solution(self):
        self.declare(ProblemFact(description= "heating-door security malfunction"))
        self.add_message('door',
                         "Unplug the device IMMEDIATELY, heating shouldn't be on while door opened")
        self.add_message('door',
                         "Contact authorized service center")
        
    @Rule(NOT(ProblemFact(description= "power off")),
          ProblemFact(lighting= "on"),
          AND(ProblemFact(door= "closed"), ProblemFact(heating= "off")))
    def lighting_malfunction_solution(self):
        self.declare(ProblemFact(description= "lighting on malfunction"))
        self.add_message('lighting',
                         "Lighting is malfunctioning, shouldn't be on with closed door and while not heating")
        self.add_message('lighting',
                         "Contact authorized service center")
        


if __name__ == "__main__":
    pass