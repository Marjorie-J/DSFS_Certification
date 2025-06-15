import plotly.graph_objects as go
import streamlit as st

from utils.common import load_data, plot_checkin_thresholds


st.markdown("# Recherche d'un seuil : délai minimum entre 2 locations🔬")

st.markdown("""Chaque location rendue en retard met potentiellement en danger la location suivante.

Une fonctionnalité imposant un délai minimum entre deux réservations peut absorber ce retard et éviter l’annulation ou la dégradation de l’expérience du prochain locataire.

- 🛟 Si le retard est inférieur au délai minimum, la location suivante peut être sauvée (le délai absorbe le retard). 

- ⛔ Si le retard est supérieur au délai minimum, la location suivante serait encore à risque. """)


# Load data
data_getaround = load_data()

st.markdown("#### Combien de cas problématiques seraient résolus en fonction du seuil choisi et du type de location ?")

# Je vais tester plusieurs seuils : de 5 minutes à 100 minutes, toutes les 5 minutes
thresholds = list(range(0, 105, 5))

plot_checkin_thresholds(
    data=data_getaround,
    thresholds=thresholds,
    column="overlap",
    y_label="Nombre de locations affectées",
    title="Nombre de locations problématiques affectées par type de checkin selon le seuil",
    percentage=False
)

# Nombre de cas problématiques 
has_pb = (data_getaround["problem"] == True)
percent_problem = has_pb.sum() / data_getaround.shape[0] * 100

st.markdown(f"""
            ⚠️ Pour rappel c'est un échantillon de {percent_problem:.2f}% des données totales.
            
            *Cet échantillon est faible et ne me permet pas de tirer de conclusion.*
            """)

st.markdown("📊 Afin d'avoir un échantillon plus important, analysons l'ensemble des locations, selon le retard au retour de location.")


st.divider()


st.subheader("Combien de locations seraient affectées en fonction du seuil choisi et du type de location ?")
st.subheader("Quelle part de revenus serait affectée par cette nouvelle fonctionnalité ?")

plot_checkin_thresholds(
    data=data_getaround,
    thresholds=thresholds,
    column="delay_at_checkout_in_minutes",
    y_label="Nombre de locations affectées",
    title="NOMBRE de locations affectées par type de checkin selon le seuil",
    percentage=False
)

plot_checkin_thresholds(
    data=data_getaround,
    thresholds=thresholds,
    column="delay_at_checkout_in_minutes",
    y_label="Pourcentage de locations sauvées",
    title="POURCENTAGE de locations sauvées par type de checkin selon le seuil",
    percentage=True
)



st.markdown("""On constate que type checkin `mobile` est beaucoup plus concerné par les retards que Connect.
        
Un seuil mis en place sur ce type de checkin permettrai d'absorber une part importante des retards :` 82%` . """)

