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

def get_empirical_avg_metal_plates_per_day(logs: pd.DataFrame) -> np.ndarray:
    logs["metal_plate"] = logs["Event"].apply(lambda x: 1 if x == "EV_ACCIDENT" else 0)
    avg_metal_plates_per_day = pd.DataFrame()
    for day in range(1, 16 + 1):
        day_incidents = logs[logs['Day'] == day].groupby("Ship").sum()["metal_plate"]
        
        avg_metal_plates_per_day = pd.concat([avg_metal_plates_per_day, pd.DataFrame({
            "Day": [day],
            "mean_metal_plates": [day_incidents.mean()]
        })])

    avg_metal_plates_per_day = avg_metal_plates_per_day.reset_index(drop=True)
    return avg_metal_plates_per_day["mean_metal_plates"].to_numpy()

def simulate_avg_metal_plates_per_day_given_parameters(x: float, y: float, nb_days: int = 16, nb_daedaluses: int = 1000) -> np.ndarray:
    daedaluses = [Daedalus(x, y) for _ in range(nb_daedaluses)]
    print(f"Simulating {nb_daedaluses} daedaluses with parameters ({x}, {y}) for {nb_days} days...")
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
    return opt.direct(objective_function, bounds=[(0.10, 0.2), (0.15, 0.25)], args=(empirical_data,))

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
    
        