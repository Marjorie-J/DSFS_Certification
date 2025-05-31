import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

### Config
st.set_page_config(
    page_title="GetAround Analysis",
    layout="wide"
)

st.title("GetAround Web Dashboard 🚗")


st.markdown("""
    Bienvenue sur le Web Dashboard GetAround !
            
    Vous y trouverez une analyse des données visant à mieux comprendre et discuter les retards lors des retours de véhicules (checkout).
            
    Ce tableau de bord vous aidera à définir un délai minimum entre deux locations, et à déterminer :

    - Le seuil : quelle durée minimale doit être appliquée entre deux réservations ?
        
    - Le périmètre : cette règle doit-elle s’appliquer à l’ensemble des véhicules ?    
""")