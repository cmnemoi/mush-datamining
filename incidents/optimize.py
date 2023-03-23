from streamlit import cache_data
from tqdm import tqdm

import numpy as np
import pandas as pd
import scipy.optimize as opt

from data import load_empricial_avg_metal_plates_per_day
from Daedalus import Daedalus

def count_nb_metal_plate_per_day_for_daedalus(daedalus: Daedalus) -> dict:
    nb_metal_plates_per_day = {day: 0 for day in [day.split(".")[0] for day in daedalus.incidentsHistory.keys()]}
    for date, incidents in daedalus.incidentsHistory.items():
        day = date.split(".")[0]
        nb_metal_plates_per_day[day] += incidents.count("Metal plate")
    return nb_metal_plates_per_day

@cache_data()
def get_empirical_avg_metal_plates_per_day(max_day: int, add_survie_ships: bool) -> np.ndarray:
    return load_empricial_avg_metal_plates_per_day(add_survie_ships)[:max_day]

def get_estimated_avg_metal_plates_per_day(max_day: int, add_survie_ships: bool) -> float:
    result = opt.curve_fit(lambda x, a, b, c: a * np.power(x, b) + c, np.arange(1, max_day + 1), get_empirical_avg_metal_plates_per_day(max_day, add_survie_ships))
    return result[0][0] * np.arange(1, max_day + 1, 1) ** result[0][1] + result[0][2]

@cache_data()
def simulate_avg_metal_plates_per_day_given_parameters(
        nb_heroes_alive: int = 11.57,
        daily_ap_consumption: int = 128.1956,
        nb_days: int = 81, 
        nb_daedaluses: int = 1000
    ) -> np.ndarray:
    daedaluses = [Daedalus(nb_heroes_alive, daily_ap_consumption) for _ in range(nb_daedaluses)]
    print(f"Simulating {nb_daedaluses} daedaluses for {nb_days} days...")
    for daedalus in tqdm(daedaluses):
        for _ in range(nb_days * 8):
            daedalus.change_cycle(print_incidents=False)
    nb_metal_plates_per_day = [count_nb_metal_plate_per_day_for_daedalus(daedalus) for daedalus in daedaluses]
    
    return pd.DataFrame(nb_metal_plates_per_day).mean()
    
def objective_function(x: np.ndarray, empirical_data) -> float:
    simulated_avg_metal_plates_per_day = simulate_avg_metal_plates_per_day_given_parameters(x[0], x[1], nb_daedaluses=100)
    mse = np.sum((empirical_data - simulated_avg_metal_plates_per_day) ** 2)
    print(f'MSE: {mse}')
    return mse

def optimize_parameters(empirical_data: np.ndarray) -> np.ndarray:
    return opt.direct(objective_function, bounds=[(0., 1), (0., 1)], args=(empirical_data,), maxiter=100)

if __name__ == "__main__":
    pass
    
        