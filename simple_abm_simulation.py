from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# Define an Agent class
class MyAgent(Agent):
    """ An agent with a fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_active = True  # Example attribute

    def step(self):
        # Example behavior: toggle the active state
        self.is_active = not self.is_active

# Define the agent portrayal method
def agent_portrayal(agent):
    """ This function dictates how agents are visually represented in the simulation."""
    portrayal = {
        "Shape": "circle",
        "Color": "blue" if agent.is_active else "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5
    }
    return portrayal

# Define the model
class MyModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.grid = MultiGrid(10, 10, True)
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MyAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(10)
            y = self.random.randrange(10)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()

# Set up the visualization
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(MyModel,
                       [grid],
                       "My Model",
                       {"N":10})  
server.launch()
