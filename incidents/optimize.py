from streamlit import cache_data
from tqdm import tqdm

import numpy as np
import pandas as pd
import scipy.optimize as opt
import optuna

from data import load_empricial_metal_plates_indicators_per_day
from Daedalus import Daedalus

def count_nb_metal_plate_per_day_for_daedalus(daedalus: Daedalus) -> dict:
    nb_metal_plates_per_day = {day: 0 for day in [day.split(".")[0] for day in daedalus.incidentsHistory.keys()]}
    for date, incidents in daedalus.incidentsHistory.items():
        day = date.split(".")[0]
        nb_metal_plates_per_day[day] += incidents.count("Metal plate")
    return nb_metal_plates_per_day

@cache_data()
def get_empirical_avg_metal_plates_per_day(max_day: int, add_survie_ships: bool) -> np.ndarray:
    empirical_metal_plates_indicators = load_empricial_metal_plates_indicators_per_day(add_survie_ships)
    return empirical_metal_plates_indicators["mean_metal_plates"].values[:max_day]

@cache_data()
def get_empirical_metal_plates_indicators_per_day(max_day: int, add_survie_ships: bool) -> pd.DataFrame:
    empirical_metal_plates_indicators = load_empricial_metal_plates_indicators_per_day(add_survie_ships)
    return empirical_metal_plates_indicators.loc[:max_day - 1]

def get_estimated_avg_metal_plates_per_day(max_day: int, add_survie_ships: bool) -> float:
    result = opt.curve_fit(lambda x, a, b, c: a * np.power(x, b) + c, np.arange(1, max_day + 1), get_empirical_avg_metal_plates_per_day(max_day, add_survie_ships))
    return result[0][0] * np.arange(1, max_day + 1, 1) ** result[0][1] + result[0][2]

@cache_data()
def simulate_avg_metal_plates_per_day_given_parameters(
        nb_heroes_alive: int,
        daily_ap_consumption,
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
    
def objective_function(x: np.ndarray, empirical_data) -> float:
    simulated_avg_metal_plates_per_day = simulate_avg_metal_plates_per_day_given_parameters(x[0], x[1], 16, nb_daedaluses=100)
    rmse = np.sqrt(np.mean((empirical_data - simulated_avg_metal_plates_per_day) ** 2))
    return rmse

if __name__ == "__main__":
    study = optuna.create_study(direction="minimize")
    study.optimize(lambda trial: objective_function(
        [trial.suggest_float("nb_heroes_alive", 11.5, 13.5),
         trial.suggest_float("daily_ap_consumption", 160., 170.)
         ], get_empirical_avg_metal_plates_per_day(16, add_survie_ships=False)), 
         n_trials=100,
    )

    print(f"Best parameters: {study.best_params}")
    print(f"RMSE = {study.best_value}")
    
        