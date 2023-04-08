from plotly import graph_objects as go
from plotly import express as px

import numpy as np
import streamlit as st

import SimulationService
import StatsService

st.title("Experimentation avec la formule des incidents de Mush")
st.warning("Attention : les données observées au delà du jour 16 sont très imprécises et doivent être considérées avec prudence.")

nb_daedaluses = st.slider("Nombre de vaisseaux à simuler (+ de vaisseaux = meilleure simulation mais chargement plus long)", 100, 1000, 100, step=100)

add_survie_ships = st.checkbox('Prendre en compte les vaisseaux "survie"', value=False)
if add_survie_ships:
    max_day = st.slider("Simuler jusqu'au jour", 1, 81, 81)
else:
    max_day = st.slider("Simuler jusqu'au jour", 1, 27, 16)

days_elapsed = np.arange(1, max_day+1)
cycles_elapsed = days_elapsed * 8

empirical_data = SimulationService.get_empirical_metal_plates_indicators_per_day(max_day, add_survie_ships)
empirical_data["lower_bound"], empirical_data["upper_bound"] = StatsService.compute_confidence_interval(empirical_data["mean_metal_plates"], empirical_data["std_metal_plates"], empirical_data["n"], 0.99)
empirical_avg_metal_plates = empirical_data["mean_metal_plates"].to_numpy()
simulated_data = SimulationService.simulate_avg_metal_plates_per_day_given_parameters(
    nb_heroes_alive=SimulationService.get_empirical_nb_heroes_alive_per_day(max_day, add_survie_ships),
    daily_ap_consumption=SimulationService.get_empirical_ap_spent_per_day(max_day, add_survie_ships),
    nb_days=max_day,
    nb_daedaluses=nb_daedaluses
)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=days_elapsed, 
    y=empirical_avg_metal_plates, 
    name="Observé",
))
fig.add_trace(go.Scatter(
    name="Intervalle de confiance (99%)",
    x=days_elapsed,
    y=empirical_data["upper_bound"],
    marker=dict(color="#444"),
    line=dict(width=0),
    mode='lines',
    fillcolor='rgba(68, 68, 68, 0.3)',
    fill='tonexty',
    hoverinfo="skip",
    showlegend=True
))
fig.add_trace(go.Scatter(
        name="Lower Bound",
        x=days_elapsed,
        y=empirical_data["lower_bound"],
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        hoverinfo="skip",
        showlegend=False
    )
)
fig.add_trace(go.Scatter(x=days_elapsed, y=simulated_data, name="Simulé"))
fig.update_layout(
    title="Nombre de plaques métalliques moyen en fonction du jour",
    xaxis_title="Jour",
    yaxis_title="Nombre de plaques métalliques moyen",
)
# add MAE and RMSE on the graph
fig.add_annotation(
    x=max_day / 2,
    y=empirical_avg_metal_plates.max(),
    text=f"RMSE: {np.sqrt(np.mean((empirical_avg_metal_plates - simulated_data) ** 2)):.2f}",
    showarrow=False
)
fig.add_annotation(
    x=max_day / 2,
    y=empirical_avg_metal_plates.max() - empirical_avg_metal_plates.std() / 4,
    text=f"MAE: {np.mean(np.abs(empirical_avg_metal_plates - simulated_data)):.2f}",
    showarrow=False
)
st.plotly_chart(fig)
