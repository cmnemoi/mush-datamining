import random

from DaedalusIncident import DaedalusIncident

class Daedalus():
    def __init__(self, x: int, y: int):
        self.day = 1
        self.cycle = 0
        self.incidents_points = 0
        self.incidents = [
            DaedalusIncident(name="Fire", weight=6, decayPoints=4),
            DaedalusIncident(name="Door blocked", weight=10, decayPoints=3),
            DaedalusIncident(name="Piece of equipment broken", weight=3, decayPoints=3),
            DaedalusIncident(name="Oxygen leak", weight=3, decayPoints=3),
            DaedalusIncident(name="Peanutz favorite event", weight=3, decayPoints=3),
            DaedalusIncident(name="Tremor", weight=10, decayPoints=2),
            DaedalusIncident(name="Metal plate", weight=3, decayPoints=2),
            DaedalusIncident(name="Electric arc", weight=3, decayPoints=8),
            DaedalusIncident(name="Disease", weight=3, decayPoints=3),
            DaedalusIncident(name="Panic attack", weight=5, decayPoints=2),
        ]
        self.incidentsHistory = {}
        self.CONSTANTE_1 = x
        self.CONSTANTE_2 = y

    def change_cycle(self, print_incidents=True):
        self.cycle += 1
        self.incidents_points = self.CONSTANTE_1 * self.__get_nb_cycles_elapsed__() + self.CONSTANTE_2
        self.__change_day__()
        cycle_incidents = self.__draw_cycle_incidents__()
        if print_incidents:
            print(f'{self} incidents:')
            for cycle_incident in cycle_incidents:
                print(cycle_incident)
        self.incidentsHistory[str(self.day) + "." + str(self.cycle)] = [str(incident) for incident in cycle_incidents]
        
    def __change_day__(self):
        if self.cycle > 8:
            self.cycle = 1
            self.day += 1

    def __draw_cycle_incidents__(self):
        cycle_incidents = []
        while self.incidents_points > 0:
            incident = random.choices(self.incidents, weights=[incident.weight for incident in self.incidents], k=1)[0]
            if incident.decayPoints > self.incidents_points:
                break
            cycle_incidents.append(incident)
            self.incidents_points -= incident.decayPoints
        return cycle_incidents
    
    def __get_nb_cycles_elapsed__(self):
        return (self.day - 1) * 8 + self.cycle

    def __str__(self) -> str:
        return f"Day {self.day} Cycle {self.cycle}"
    