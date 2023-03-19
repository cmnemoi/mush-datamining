import os
import shutil

import pandas as pd

def find_event_name_by_log_content(logs: pd.DataFrame, content: str, n: int = 100000) -> str:
    """
    Function to find the name of an event given a sub string contained in its log (must be unique)
     
    For example `find_event_name_by_log_content("crochet du droit")` returns "FIST_WOUNDED"

    Parameters :
    ------------
    content : str
        Sub string contained in the log
    n : int
        Number of logs to search in the dataset
    """
    event_name_found = False
    
    while not event_name_found:
        sample = logs.sample(n)
        for i in sample.index.to_list():
            if content in sample.loc[i, "Log"]:
                return sample.loc[i, "Event"]

def find_all_events_by_name(logs: pd.DataFrame, event_name: str) -> pd.DataFrame:
    """
    Function to find all the logs of a given event name

    Parameters :
    ------------
    event_name : str
        Name of the event to find
    """
    return logs[logs["Event"] == event_name]

def get_ship_logs(logs: pd.DataFrame, id_ship: int) -> pd.DataFrame:
    """
    Function to get all the logs of a given ship

    Parameters :
    ------------
    id_ship : int
        Id of the ship to get the logs from
    """
    return logs[logs["Ship"] == id_ship]

def get_character_logs(logs: pd.DataFrame, character: str) -> pd.DataFrame:
    """
    Function to get all the logs of a given character

    Parameters :
    ------------
    character : str
        Character name to get the logs from
    """
    return logs[logs["Character"] == character]

def get_cycle_of_day_logs(logs: pd.DataFrame, cycle: float) -> pd.DataFrame:
    """
    Function to get all the logs of a given cycle of day

    Parameters :
    ------------
    cycle : float
        Cycle number (X.Y) to get the logs from
    """
    return logs[logs["Day.Cycle"] == cycle]

def get_logs_before_cycle_of_day(logs: pd.DataFrame, cycle: float) -> pd.DataFrame:
    """
    Function to get all the logs before a given cycle of day

    Parameters :
    ------------
    cycle : float
        Cycle number (X.Y) to get the logs before
    """
    return logs[logs["Day.Cycle"] <= cycle]

def get_logs_after_cycle_of_day(logs: pd.DataFrame, cycle: float) -> pd.DataFrame:
    """
    Function to get all the logs after a given cycle of day

    Parameters :
    ------------
    cycle : float
        Cycle number (X.Y) to get the logs after
    """
    return logs[logs["Day.Cycle"] >= cycle]

def load_player_logs() -> pd.DataFrame:
    """
    Function to load all the player logs in a DataFrame from CSV or ZIP

    Returns :
    ---------
    logs : pd.DataFrame
        Dataframe containing all the player logs
    """
    if not os.path.exists("data/player_logs.csv"):
        shutil.unpack_archive("data/player_logs.zip", "/data/")

    return pd.read_csv("data/player_logs.csv")