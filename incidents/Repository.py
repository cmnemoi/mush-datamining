from google.oauth2.service_account import Credentials
from streamlit import cache_data, secrets

import pandas as pd

GCP_SERVICE_ACCOUNT = secrets.gcp_service_account

@cache_data()
def load_empricial_metal_plates_indicators_per_day(add_survie_ships: bool) -> pd.DataFrame:
    metal_plates_indicators = pd.read_gbq(
        query=f"""
        WITH t AS (
            SELECT Ship, Day, SUM(metal_plate_event) AS metal_plates FROM `{GCP_SERVICE_ACCOUNT.project_id}.mush.player_logs`
            WHERE is_survie_ship = {str(add_survie_ships)}
            GROUP BY Ship, Day
        )
        SELECT Day, AVG(t.metal_plates) AS mean_metal_plates, STDDEV(t.metal_plates) AS std_metal_plates, COUNT(*) AS n
        FROM t
        WHERE Day IS NOT NULL
        GROUP by Day
        ORDER BY Day
        """,
        credentials=Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT),
    )
    metal_plates_indicators = metal_plates_indicators.reset_index(drop=True)
    return metal_plates_indicators

@cache_data()
def load_ap_spent_per_day(add_survie_ships: bool) -> pd.DataFrame:
    ap_spent_per_day = pd.read_gbq(
        query=f"""
        WITH t AS (
            SELECT Ship, Day, SUM(event_ap_cost) AS event_ap_cost FROM `{GCP_SERVICE_ACCOUNT.project_id}.mush.player_logs`
            WHERE is_survie_ship = {str(add_survie_ships)} AND event_ap_cost IS NOT NULL
            GROUP BY Ship, Day
        )
        SELECT Day, AVG(t.event_ap_cost) AS mean_ap_spent, STDDEV(t.event_ap_cost) AS std_ap_spent, COUNT(*) AS n
        FROM t
        WHERE Day IS NOT NULL
        GROUP by Day
        ORDER BY Day
        """,
        credentials=Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT),
    )
    ap_spent_per_day = ap_spent_per_day.reset_index(drop=True)
    return ap_spent_per_day

@cache_data()
def load_nb_heroes_alive_per_day(add_survie_ships: bool) -> pd.DataFrame:
    nb_heroes_alive_per_day = pd.read_gbq(
        query=f"""
        WITH t AS (
            SELECT Ship, Day, COUNT(DISTINCT Character) AS nb_heroes_alive FROM `{GCP_SERVICE_ACCOUNT.project_id}.mush.player_logs`
            WHERE is_survie_ship = {str(add_survie_ships)}
            GROUP BY Ship, Day
        )
        SELECT Day, AVG(t.nb_heroes_alive) AS mean_nb_heroes_alive, STDDEV(t.nb_heroes_alive) AS std_nb_heroes_alive, COUNT(*) AS n
        FROM t
        WHERE Day IS NOT NULL
        GROUP by Day
        ORDER BY Day
        """,
        credentials=Credentials.from_service_account_info(GCP_SERVICE_ACCOUNT),
    )

    nb_heroes_alive_per_day = nb_heroes_alive_per_day.reset_index(drop=True)
    return nb_heroes_alive_per_day
