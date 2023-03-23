from streamlit import cache_data
from tqdm import tqdm

import numpy as np
import pandas as pd

from Daedalus import Daedalus
import Repository

def count_nb_metal_plate_per_day_for_daedalus(daedalus: Daedalus) -> dict:
    nb_metal_plates_per_day = {day: 0 for day in [day.split(".")[0] for day in daedalus.incidentsHistory.keys()]}
    for date, incidents in daedalus.incidentsHistory.items():
        day = date.split(".")[0]
        nb_metal_plates_per_day[day] += incidents.count("Metal plate")
    return nb_metal_plates_per_day

def get_empirical_avg_metal_plates_per_day(max_day: int, add_survie_ships: bool) -> np.ndarray:
    empirical_metal_plates_indicators = Repository.load_empricial_metal_plates_indicators_per_day(add_survie_ships)
    return empirical_metal_plates_indicators["mean_metal_plates"].values[:max_day]

def get_empirical_metal_plates_indicators_per_day(max_day: int, add_survie_ships: bool) -> pd.DataFrame:
    empirical_metal_plates_indicators = Repository.load_empricial_metal_plates_indicators_per_day(add_survie_ships)
    return empirical_metal_plates_indicators.loc[:max_day - 1]

def get_empirical_ap_spent_per_day(max_day: int, add_survie_ships: bool) -> pd.DataFrame:
    ap_spent_per_day = Repository.load_ap_spent_per_day(add_survie_ships)
    return ap_spent_per_day.loc[:max_day - 1]

def get_empirical_nb_heroes_alive_per_day(max_day: int, add_survie_ships: bool) -> pd.DataFrame:
    nb_heroes_alive_per_day = Repository.load_nb_heroes_alive_per_day(add_survie_ships)
    return nb_heroes_alive_per_day.loc[:max_day - 1]

def simulate_avg_metal_plates_per_day_given_parameters(
        nb_heroes_alive: int,
        daily_ap_consumption: float,
        nb_days: int, 
        nb_daedaluses: int = 1000
    ) -> np.ndarray:
    daedaluses = [Daedalus(nb_heroes_alive, daily_ap_consumption) for _ in range(nb_daedaluses)]
    print(f"Simulating {nb_daedaluses} daedaluses for {nb_days} days...")
    for daedalus in tqdm(daedaluses):
        for _ in range(nb_days * 8):
            daedalus.change_cycle(print_incidents=False)
    nb_metal_plates_per_day = [count_nb_metal_plate_per_day_for_daedalus(daedalus) for daedalus in daedaluses]
    
    return pd.DataFrame(nb_metal_plates_per_day).mean()
