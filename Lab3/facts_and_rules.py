from experta import Fact, KnowledgeEngine, Rule, Field, NOT, OR

SEPARATOR = '-' * 70

class ProblemFact(Fact):
    """provides information about microwave state,
       used by expert system to check the rules conditions"""
    pass
    

class MicrowaveExpertSystem(KnowledgeEngine):
    # no power rules
    @Rule(ProblemFact(power= "off"))
    def no_power_solution(self):
        self.declare(ProblemFact(description= "power off"))
        print("Check if the power cable is connected to the power plug")
    
    # no heating rules   
    @Rule(NOT(ProblemFact(description= "power off")),
          ProblemFact(heating= "off"))
    def no_heating_problem(self):
        self.declare(ProblemFact(description= "heating off"))
      
    @Rule(ProblemFact(description= "heating off"),
          ProblemFact(door= "open"))
    def no_heating_open_door_solution(self):
        self.declare(ProblemFact(description= "door open"))
        print("Close the microwave door before turning heating on")
        
    @Rule(ProblemFact(description= "heating off"),
          NOT(ProblemFact(description= "door open")),
          ProblemFact(start_button= "off"))
    def no_heating_closed_door_solution(self):
        self.declare(ProblemFact(description= "start button not clicked"))
        print("Set the desired heating time and click start button to start the heating")
        
    @Rule(ProblemFact(description= "heating off"),
          NOT(ProblemFact(description= "door open")),
          ProblemFact(start_button= "on"))
    def no_heating_closed_door_start_on_solution(self):
        self.declare(ProblemFact(description= "heating broken"))
        print("Try unplugging and pluging the power cable back to the power plug")
        print("If the microwave still doesn't turn on the heating, contact authorized service center")
    
    # display off rules 
    @Rule(NOT(ProblemFact(description= "power off")),
          ProblemFact(display= "off"))
    def display_off_power_on_solution(self):
        self.declare(ProblemFact(description= "display off"))
        print("Try unplugging and pluging the power cable back to the power plug")
        print("If the display is still off, contact authorized service center")
    
    # lighting off rules
    @Rule(NOT(ProblemFact(description= "power off")),
          ProblemFact(lighting= "off"))
    def lighting_off_problem(self):
        self.declare(ProblemFact(description= "lighting off"))
        
    @Rule(ProblemFact(description= "lighting off"),
          ProblemFact(description="heating off"),
          ProblemFact(door= "closed"))
    def lighting_off_solution(self):
        self.declare(ProblemFact(description= "lighting off door closed"))
        print("Open the door or start heating process to trigger the lighting on")
        
    @Rule(ProblemFact(description="lighting off"),
          OR(ProblemFact(door= "open"), ProblemFact(heating= "on")))
    def lighting_off_broken_solution(self):
        self.declare(ProblemFact(description= "lighting off broken"))
        print("Lighting is not working, the bulb needs replacing")
        print("Contact authorized service center to change the bulb")


if __name__ == "__main__":
    pass