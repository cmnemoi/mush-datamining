import os
import shutil

import pandas as pd

def find_action_name_by_log_content(logs: pd.DataFrame, content: str, n: int = 100000) -> str:
    """
    Function to find the name of an action given a sub string contained in its log (must be unique)
     
    For example `find_action_name_by_log_content("crochet du droit")` returns "FIST_WOUNDED"

    Parameters :
    ------------
    content : str
        Sub string contained in the log
    n : int
        Number of logs to search in the dataset
    """
    action_name_found = False
    
    while not action_name_found:
        sample = logs.sample(n)
        for i in sample.index.to_list():
            if content in sample.loc[i, "Log"]:
                return sample.loc[i, "Action"]

def find_all_actions_by_name(logs: pd.DataFrame, action_name: str) -> pd.DataFrame:
    """
    Function to find all the logs of a given action name

    Parameters :
    ------------
    action_name : str
        Name of the action to find
    """
    return logs[logs["Action"] == action_name]

def get_player_logs() -> pd.DataFrame:
    """
    Function to get all the player logs in a DataFrame

    Returns :
    ---------
    logs : pd.DataFrame
        Dataframe containing all the player logs
    """
    if not os.path.exists("../data/clean_player_logs.csv"):
        shutil.unpack_archive("../data/clean_player_logs.zip", "../data/")

    return pd.read_csv("../data/clean_player_logs.csv", sep=";")