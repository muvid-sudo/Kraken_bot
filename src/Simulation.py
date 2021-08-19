

class Simulation:
    budget = 0.0
    positions = []


    def __init__(self, budget):
        self.budget = budget


    def add_position(self, position):
        self.positions.append(position)
        self.budget -= position.get_position_cost()
    
    def get_budget(self):
        return self.budget


    def get_positions(self):
        return self.positions



