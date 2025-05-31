import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="GetAround Web Dashboard 🚗", layout="wide")

from utils.common import data_getaround

st.markdown("# Enchainemenet des locations ⏭️")


## Cas problématiques
st.subheader("Analyse des cas problématiques : La voiture de la location précédente a été rendue après le début de la location suivante.")

# Chevauchement potentiel
fig = px.histogram(data_getaround, x="overlap", color="problem", color_discrete_map={True: "red"},
                   labels={'overlap': 'Chevauchement (min)'},
                   title="Chevauchement entre deux locations. Plus le chevauchement est négatif, plus il est sévère.",
                   color_discrete_sequence=px.colors.qualitative.Bold)
fig.update_layout(yaxis_title=None, yaxis=dict(tickformat='d'), showlegend=False)
st.plotly_chart(fig, use_container_width=True)


# Nombre de cas problématiques 
has_pb = (data_getaround["problem"] == True)
percent_problem = has_pb.sum() / data_getaround.shape[0] * 100

st.markdown(f"""⚠️ Les cas problématiques représentent {percent_problem:.2f}% des données.""")


fig = px.box(data_getaround, x="checkin_type", y="overlap", color="checkin_type",
    labels={'overlap': 'Chevauchement (min)', 'checkin_type': 'Type de check-in'},
    title="Chevauchement par type de check-in", 
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
            Pour rappel une valeur négative signifie qu'une location a été rendue après le début de la location suivante.
            
            On observe donc un chevauchement plus important pour les location `mobile`.
            """)