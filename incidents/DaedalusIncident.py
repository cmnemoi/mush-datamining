class DaedalusIncident():
    def __init__(self, name: str, weight: int, decayPoints: int):
        self.name = name
        self.weight = weight
        self.decayPoints = decayPoints
        
    def __str__(self):
        return self.name