from google.oauth2.service_account import Credentials
from streamlit import cache_data, secrets

import pandas as pd

@cache_data()
def load_empricial_avg_metal_plates_per_day():
    gcp_service_account = secrets.gcp_service_account
    avg_metal_plates_per_day = pd.read_gbq(
        query=f"""
        WITH t AS (
            SELECT Ship, Day, SUM(metal_plate_event) AS metal_plates FROM `avian-sunlight-350718.mush.player_logs`
            GROUP BY Ship, Day
        )
        SELECT Day, AVG(t.metal_plates) AS mean_metal_plates 
        FROM t
        WHERE Day IS NOT NULL
        GROUP by Day
        ORDER BY Day
        """,
        credentials=Credentials.from_service_account_info(gcp_service_account),
    )

    avg_metal_plates_per_day = avg_metal_plates_per_day.reset_index(drop=True)
    return avg_metal_plates_per_day["mean_metal_plates"].to_numpy()

if __name__ == "__main__":
    pass