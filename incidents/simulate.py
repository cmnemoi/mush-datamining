import pandas as pd

from Daedalus import Daedalus

def count_type_of_incidents_per_day_for_daedalus(daedalus: Daedalus):
    incidents_per_day = pd.DataFrame(columns=["day"] + [incident.name for incident in daedalus.incidents])
    for date, incidents in daedalus.incidentsHistory.items():
        day = int(date.split(".")[0])
        incidents_per_day = incidents_per_day.append(
            {"day": day, **{incident.name: incidents.count(incident.name) for incident in daedalus.incidents}}, 
            ignore_index=True
        )
    return incidents_per_day.groupby("day").sum()

if __name__ == "__main__":
    daedalus = Daedalus(
        nb_heroes_alive=11.57,
        daily_ap_consumption=128.1956
    )
    for _ in range(20 + 1):
        daedalus.change_cycle(False)

    print(count_type_of_incidents_per_day_for_daedalus(daedalus))