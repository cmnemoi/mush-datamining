import random

from DaedalusIncident import DaedalusIncident

class Daedalus():
    def __init__(self, nb_heroes_alive = 0, daily_ap_consumption = 0):
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
        self.C2 = 0.5
        self.nb_heroes_alive = nb_heroes_alive
        self.daily_AP_consumption = daily_ap_consumption
        self.HARD_MODE_START_DAY = 4
        self.VERY_HARD_MODE_START_DAY = 9
        self.BASE_INCIDENT_POINTS_THRESHOLD = 18        

    def change_cycle(self, print_incidents=True):
        self.__update_daedalus_stats__()
        self.__update_incident_points__(self.__compute_incidents_points_to_add__())
        print(f'{self} incidents points: {self.incidents_points}')
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

    def __compute_incidents_points_to_add__(self) -> int:
        points_to_add = 0
        match self.day:
            case 1:
                points_to_add += 1
            case 2:
                points_to_add += 2
            case other:
                points_to_add += 1
                hard_mode_malus = self.day - 1 - self.HARD_MODE_START_DAY
                very_hard_mode_malus = self.day - 1 - self.VERY_HARD_MODE_START_DAY
                if self.day >= self.HARD_MODE_START_DAY:
                    points_to_add += 1 + hard_mode_malus
                elif self.day >= self.VERY_HARD_MODE_START_DAY:
                    points_to_add += 3 + hard_mode_malus + very_hard_mode_malus

        return points_to_add


    def __draw_cycle_incidents__(self):
        launch_incidents = random.random() <= (self.incidents_points / self.BASE_INCIDENT_POINTS_THRESHOLD)
        if not launch_incidents:
            return []
        incidents_to_draw = self.incidents.copy()
        cycle_incidents = []
        upper_bound = 2000
        while self.incidents_points > 0 and len(incidents_to_draw) > 0 and upper_bound > 0:
            upper_bound -= 1
            incident = random.choices(incidents_to_draw, weights=[incident.weight for incident in incidents_to_draw], k=1)[0]
            if incident.decayPoints > self.incidents_points:
                incidents_to_draw.remove(incident)
                continue
            cycle_incidents.append(incident)
            self.incidents_points -= incident.decayPoints

        return cycle_incidents
    
    def __get_overload_factor__(self) -> float:
        threshold = 7 * self.nb_heroes_alive
        return self.daily_AP_consumption / threshold if self.daily_AP_consumption > threshold else 1

    def __str__(self) -> str:
        return f"Day {self.day} Cycle {self.cycle}"
    
    def __update_incident_points__(self, points_to_add: int):
        points_to_add = int(points_to_add * self.__get_overload_factor__() + self.C2)
        self.incidents_points += points_to_add

    def __update_daedalus_stats__(self):
        self.cycle += 1
        self.__change_day__()