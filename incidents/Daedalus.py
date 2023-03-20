import random

from DaedalusIncident import DaedalusIncident

class Daedalus():
    def __init__(self, c1: int, c2: int, nb_heroes_alive = 0, daily_ap_consumption = 0, incidentPointsRatioToSpend = 0.5):
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
        self.c1 = c1
        self.c2 = c2
        self.nb_heroes_alive = nb_heroes_alive
        self.daily_AP_consumption = daily_ap_consumption
        self.incidentPointsRatioToSpend = incidentPointsRatioToSpend
        

    def change_cycle(self, print_incidents=True):
        self.__update_daedalus_stats__()
        self.__update_incident_points__()
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
        incidents_to_draw = self.incidents.copy()
        cycle_incidents = []
        while self.incidents_points * self.incidentPointsRatioToSpend > 0 and len(incidents_to_draw) > 0:
            incident = random.choices(incidents_to_draw, weights=[incident.weight for incident in incidents_to_draw], k=1)[0]
            if incident.decayPoints > self.incidents_points:
                incidents_to_draw.remove(incident)
                continue
            cycle_incidents.append(incident)
            self.incidents_points -= incident.decayPoints
        return cycle_incidents
    
    def __get_nb_cycles_elapsed__(self):
        return (self.day - 1) * 8 + self.cycle

    def __str__(self) -> str:
        return f"Day {self.day} Cycle {self.cycle}"
    
    def __update_incident_points__(self):
        threshold = 7 * self.nb_heroes_alive
        overloadFactor = self.daily_AP_consumption / threshold if self.daily_AP_consumption > threshold else 1
        self.incidents_points = self.c1 * overloadFactor * self.__get_nb_cycles_elapsed__() + self.c2

    def __update_daedalus_stats__(self):
        self.cycle += 1
        self.__change_day__()