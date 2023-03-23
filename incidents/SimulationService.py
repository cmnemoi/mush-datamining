from streamlit import cache_data
from tqdm import tqdm

import numpy as np
import pandas as pd

from Daedalus import Daedalus
from Repository import Repository

class SimulationService():
    def __init__(self):
        self.repository = Repository()

    def count_nb_metal_plate_per_day_for_daedalus(_self, daedalus: Daedalus) -> dict:
        nb_metal_plates_per_day = {day: 0 for day in [day.split(".")[0] for day in daedalus.incidentsHistory.keys()]}
        for date, incidents in daedalus.incidentsHistory.items():
            day = date.split(".")[0]
            nb_metal_plates_per_day[day] += incidents.count("Metal plate")
        return nb_metal_plates_per_day

    @cache_data()
    def get_empirical_avg_metal_plates_per_day(_self, _max_day: int, _add_survie_ships: bool) -> np.ndarray:
        empirical_metal_plates_indicators = _self.repository.load_empricial_metal_plates_indicators_per_day(_add_survie_ships)
        return empirical_metal_plates_indicators["mean_metal_plates"].values[:_max_day]

    @cache_data()
    def get_empirical_metal_plates_indicators_per_day(_self, _max_day: int, _add_survie_ships: bool) -> pd.DataFrame:
        empirical_metal_plates_indicators = _self.repository.load_empricial_metal_plates_indicators_per_day(_add_survie_ships)
        return empirical_metal_plates_indicators.loc[:_max_day - 1]
    
    @cache_data()
    def get_empirical_ap_spent_per_day(_self, _max_day: int, _add_survie_ships: bool) -> pd.DataFrame:
        ap_spent_per_day = _self.repository.load_ap_spent_per_day(_add_survie_ships)
        return ap_spent_per_day.loc[:_max_day - 1]
    
    @cache_data()
    def get_empirical_nb_heroes_alive_per_day(_self, _max_day: int, _add_survie_ships: bool) -> pd.DataFrame:
        nb_heroes_alive_per_day = _self.repository.load_nb_heroes_alive_per_day(_add_survie_ships)
        return nb_heroes_alive_per_day.loc[:_max_day - 1]
    
    @cache_data()
    def simulate_avg_metal_plates_per_day_given_parameters(
            _self,
            _nb_heroes_alive: int,
            _daily_ap_consumption: float,
            _nb_days: int, 
            _nb_daedaluses: int = 1000
        ) -> np.ndarray:
        daedaluses = [Daedalus(_nb_heroes_alive, _daily_ap_consumption) for _ in range(_nb_daedaluses)]
        print(f"Simulating {_nb_daedaluses} daedaluses for {_nb_days} days...")
        for daedalus in tqdm(daedaluses):
            for _ in range(_nb_days * 8):
                daedalus.change_cycle(print_incidents=False)
        nb_metal_plates_per_day = [_self.count_nb_metal_plate_per_day_for_daedalus(daedalus) for daedalus in daedaluses]
        
        return pd.DataFrame(nb_metal_plates_per_day).mean()
    