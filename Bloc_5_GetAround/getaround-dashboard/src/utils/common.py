import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA_URL = ("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx")

## LOAD DATA
@st.cache_data
def load_data():
    data = pd.read_excel(DATA_URL)

    # Outliers delay_at_checkout_in_minutes
    valeur_palier_haut = data["delay_at_checkout_in_minutes"].mean() + 3 * data["delay_at_checkout_in_minutes"].std()
    valeur_palier_bas = data["delay_at_checkout_in_minutes"].mean() - 3 * data["delay_at_checkout_in_minutes"].std()

    outlier_condition = (data["delay_at_checkout_in_minutes"] > valeur_palier_haut) | (data["delay_at_checkout_in_minutes"] < valeur_palier_bas)
    data = data[~outlier_condition]

    # On extrait le délai de checkout pour chaque location
    delay_checkout = data[["rental_id", "delay_at_checkout_in_minutes"]].rename(
        columns={"rental_id": "previous_ended_rental_id", "delay_at_checkout_in_minutes": "previous_delay_at_checkout_in_minutes"}
    )

    # On le joint à la location suivante : afin d'avoir le délai de checkout de la location précédente
    data = data.merge(delay_checkout, on="previous_ended_rental_id", how="left")

    
    # Nous créons une colonne overlap qui représente le chevauchement potentiel entre deux locations : time_delta - delay
    # Plus overlap est négatif, plus le chevauchement est sévère.
    # Plus il est positif, plus il y a de marge de sécurité.
    data["overlap"] = data['time_delta_with_previous_rental_in_minutes'] - data["previous_delay_at_checkout_in_minutes"]

    # Problèmes
    # problem = True	= La location précédente a empiété sur celle-ci (chevauchement).
    # problem = False	= Aucun problème de timing. La voiture était prête à temps.
    data["problem"] = data["overlap"] < 0

    return data

data_getaround = load_data()


## VISUALISATION DES SEUILS
def plot_checkin_thresholds(data, thresholds, column, y_label, title, percentage=False):
    fig = go.Figure()

    # Courbes par type de checkin
    for checkin_type in data["checkin_type"].unique():
        values = []
        mask_checkin = (data["checkin_type"] == checkin_type)

        for threshold in thresholds:
            # Nombre de locations à risque, mais dont le chevauchement est absorbable par le seuil.
            count = (mask_checkin & (data[column] <= threshold) & (data[column] >= 0)).sum()

            if percentage:
                count = count / data.shape[0] * 100
            values.append(count)

        fig.add_trace(go.Scatter(x=thresholds, y=values, mode="lines+markers", name=checkin_type))

    # Courbe totale
    total_values = []
    for threshold in thresholds:
        total_count = ((data[column] <= threshold) & (data[column] >= 0)).sum()
        if percentage:
            total_count = total_count / data.shape[0] * 100
        total_values.append(total_count)

    fig.add_trace(go.Scatter(x=thresholds, y=total_values, mode="lines+markers", name="Total"))

    # Mise en page
    fig.update_layout(title=title, xaxis_title="Seuil (minutes)", yaxis_title=y_label)

    st.plotly_chart(fig, use_container_width=True)
