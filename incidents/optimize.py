from streamlit import cache_data
from tqdm import tqdm

import numpy as np
import pandas as pd
import scipy.optimize as opt

from Daedalus import Daedalus
from utils import load_player_logs

def count_nb_metal_plate_per_day_for_daedalus(daedalus: Daedalus) -> dict:
    nb_metal_plates_per_day = {day: 0 for day in [day.split(".")[0] for day in daedalus.incidentsHistory.keys()]}
    for date, incidents in daedalus.incidentsHistory.items():
        day = date.split(".")[0]
        nb_metal_plates_per_day[day] += incidents.count("Metal plate")
    return nb_metal_plates_per_day

@cache_data()
def get_empirical_avg_metal_plates_per_day(logs: pd.DataFrame, max_day: int = 16) -> np.ndarray:
    logs["metal_plate"] = logs["Event"].apply(lambda x: 1 if x == "EV_ACCIDENT" else 0)
    avg_metal_plates_per_day = pd.DataFrame()
    for day in range(1, max_day + 1):
        day_incidents = logs[logs['Day'] == day].groupby("Ship").sum()["metal_plate"]
        n = len(day_incidents)
        avg_metal_plates_per_day = pd.concat([avg_metal_plates_per_day, pd.DataFrame({
            "Day": [day],
            "mean_metal_plates": [day_incidents.mean()],
            "CI (95%)": [day_incidents.std() / np.sqrt(n) * 1.96]
        })])

    avg_metal_plates_per_day = avg_metal_plates_per_day.reset_index(drop=True)
    return avg_metal_plates_per_day["mean_metal_plates"].to_numpy()

@cache_data()
def simulate_avg_metal_plates_per_day_given_parameters(
        c1: float, 
        c2: float,
        nb_heroes_alive: int,
        daily_ap_consumption: int,
        nb_days: int = 16, 
        nb_daedaluses: int = 1000
    ) -> np.ndarray:
    daedaluses = [Daedalus(c1, c2, nb_heroes_alive, daily_ap_consumption) for _ in range(nb_daedaluses)]
    print(f"Simulating {nb_daedaluses} daedaluses with parameters ({c1}, {c2}) for {nb_days} days...")
    for daedalus in tqdm(daedaluses):
        for _ in range(nb_days * 8):
            daedalus.change_cycle(print_incidents=False)
    nb_metal_plates_per_day = [count_nb_metal_plate_per_day_for_daedalus(daedalus) for daedalus in daedaluses]
    
    return pd.DataFrame(nb_metal_plates_per_day).mean()
    
def objective_function(x: np.ndarray, empirical_data) -> float:
    simulated_avg_metal_plates_per_day = simulate_avg_metal_plates_per_day_given_parameters(x[0], x[1])
    mse = np.sum((empirical_data - simulated_avg_metal_plates_per_day) ** 2)
    print(f'MSE: {mse}')
    return mse

def optimize_parameters(empirical_data: np.ndarray) -> np.ndarray:
    return opt.direct(objective_function, bounds=[(0, 1), (0, 1)], args=(empirical_data,), maxiter=100)

if __name__ == "__main__":
    print('Loading logs...')
    logs = load_player_logs().dropna()
    logs.Day = logs.Day.astype(int)
    print('Done.')
    print('Computing empirical average metal plates per day...')
    empirical_avg_metal_plates_per_day = get_empirical_avg_metal_plates_per_day(logs)
    print('Done.')
    print('Finding parameters matching empirical average metal plates per day...')
    print(optimize_parameters(empirical_avg_metal_plates_per_day))
    
        