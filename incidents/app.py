from plotly import graph_objects as go
from plotly import express as px

import numpy as np
import streamlit as st

from optimize import (
    get_empirical_avg_metal_plates_per_day,
    get_estimated_avg_metal_plates_per_day,
    simulate_avg_metal_plates_per_day_given_parameters
)

st.title("Experimentation avec la formule des incidents de Mush")
st.warning("Attention : les données observées au delà du jour 16 sont très imprécises et doivent être considérées avec prudence.")

columns = st.columns(3)

with columns[0]:
    c1 = st.slider("Constante 1", 0., 1., step=0.001, value=0.09)
    c2 = st.slider("Constante 2", -5., 1., step=0.001, value = 0.03)
with columns[1]:
    nbHeroesAlive = st.slider("Nombre de héros en vie", 1., 16., value=11.57)
    dailyAPconsumption = st.slider("Consommation de PA journalière", 0., 600., 128.1956)
with columns[2]:
    incidentPointsRatio = st.slider("Pourentage de points d'incidents à dépenser à chaque cycle", 0, 100, step=1, value=50) / 100
    nb_daedaluses = st.slider("Nombre de vaisseaux à simuler (+ de vaisseaux = meilleure simulation mais chargement plus long)", 100, 1000, 100, step=100)

add_survie_ships = st.checkbox('Prendre en compte les vaisseaux "survie"', value=False)
if add_survie_ships:
    max_day = st.slider("Simuler jusqu'au jour", 1, 81, 81)
else:
    max_day = st.slider("Simuler jusqu'au jour", 1, 27, 16)
    

days_elapsed = np.arange(0, max_day)
cycles_elapsed = days_elapsed * 8

threshold = 7 * nbHeroesAlive
overloadFactor = dailyAPconsumption / threshold if dailyAPconsumption > threshold else 1

incidentsPoints = (cycles_elapsed * overloadFactor * c1 + c2).astype(int)

empirical_data = get_empirical_avg_metal_plates_per_day(max_day=max_day, add_survie_ships=add_survie_ships)
estimated_data = get_estimated_avg_metal_plates_per_day(max_day=max_day)
simulated_data = simulate_avg_metal_plates_per_day_given_parameters(
    c1, 
    c2,
    incidentsPointsRatio=incidentPointsRatio, 
    nb_heroes_alive=nbHeroesAlive, 
    daily_ap_consumption=dailyAPconsumption,
    nb_days=max_day,
    nb_daedaluses=nb_daedaluses
)

fig = go.Figure()
fig.add_trace(go.Scatter(x=days_elapsed, y=empirical_data, name="Observé"))
fig.add_trace(go.Scatter(x=days_elapsed, y=estimated_data, name="Estimé"))
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