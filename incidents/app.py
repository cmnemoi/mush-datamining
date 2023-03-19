from plotly import graph_objects as go
from plotly import express as px

import numpy as np
import streamlit as st

from utils import load_player_logs
from optimize import get_empirical_avg_metal_plates_per_day, simulate_avg_metal_plates_per_day_given_parameters

@st.cache_data()
def load_logs():
    logs = load_player_logs(from_sqlite_db=True).dropna()
    logs.Day = logs.Day.astype(int)
    return logs

st.title("Experimentation avec la formule des incidents de Mush")

logs = load_logs()

nbHeroesAlive = st.slider("Nombre de héros en vie", 1, 16, value=16)
dailyAPconsumption = st.slider("Consommation de PA journalière", 0, 600, 1)
c1 = st.slider("Constante 1", 0.010, 1., step=0.001, value=0.500)
c2 = st.slider("Constante 2", 0.010, 1., step=0.001, value=0.500)
max_day = st.slider("Simuler jusqu'au jour", 1, 81, 16)
st.warning("Attention : les données observées au delà du jour 16 sont très imprécises et doivent être considérées avec prudence.")

days_elapsed = np.arange(0, max_day)
cycles_elapsed = days_elapsed * 8

threshold = 7 * nbHeroesAlive
overloadFactor = dailyAPconsumption / threshold if dailyAPconsumption > threshold else 1

incidentsPoints = (cycles_elapsed * overloadFactor * c1 + c2).astype(int)

empirical_data = get_empirical_avg_metal_plates_per_day(logs, max_day=max_day)
simulated_data = simulate_avg_metal_plates_per_day_given_parameters(
    c1, 
    c2, 
    nb_heroes_alive=nbHeroesAlive, 
    daily_ap_consumption=dailyAPconsumption,
    nb_days=max_day,
)

fig = go.Figure()
fig.add_trace(go.Scatter(x=days_elapsed, y=empirical_data, name="Observé"))
fig.add_trace(go.Scatter(x=days_elapsed, y=simulated_data, name="Simulé"))
fig.update_layout(
    title="Nombre de plaques métalliques moyen en fonction du jour",
    xaxis_title="Jour",
    yaxis_title="Nombre de plaques métalliques moyen",
)
# add MAE and RMSE on the graph
fig.add_annotation(
    x=max_day / 2,
    y=empirical_data.max(),
    text=f"RMSE: {np.sqrt(np.sum((empirical_data - simulated_data) ** 2)):.2f}",
    showarrow=False
)
fig.add_annotation(
    x=max_day / 2,
    y=empirical_data.max() - empirical_data.std() / 4,
    text=f"MAE: {np.sum(np.abs(empirical_data - simulated_data)):.2f}",
    showarrow=False
)
st.plotly_chart(fig)

st.write("Formule des points d'incidents:")
st.markdown(
    """
    ```
    Si consommation de PA journalière < 7 * nombre de héros en vie alors
        multiplicateur = 1
    Sinon
        multiplicateur = consommation de PA journalière / (7 * nombre de héros en vie) 

    Points d'incidents = Nombre de cycles écoulés x multiplicateur x Constante_1 
    + Constante_2
    ```
    """
)