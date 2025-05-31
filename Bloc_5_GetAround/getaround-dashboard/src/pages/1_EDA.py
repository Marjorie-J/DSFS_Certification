import plotly.express as px
import streamlit as st

st.set_page_config(page_title="GetAround Web Dashboard 🚗", layout="wide")

from utils.common import data_getaround

st.markdown("# EDA 📈")

st.markdown("""
Bienvenue dans la section EDA ! 
            
Dans cette section, nous explorons les données de la plateforme GetAround, un service de location de voitures entre particuliers.

Vous y trouverez des visualisations et des statistiques comme notamment :
            
La répartition des informations qui ont servi à l'analyse ou l'étude des retards

Ces analyses permettent de mieux comprendre les données afin d'améliorer les décisions métier.
""")

st.divider()

## Distribution des variables
st.subheader("Visualisation des données 📈")

## Run the below code if the check is checked ✅
if st.checkbox("Visualiser les données qui ont permis cette analyse"):
    st.write(data_getaround)  

# checkin_type
df_counts = data_getaround["checkin_type"].value_counts().reset_index()
df_counts.columns = ["checkin_type", "count"]

fig = px.bar(df_counts, x="checkin_type", y="count", 
             color="checkin_type", title="Types de checkin", color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(xaxis_title=None, yaxis_title=None, yaxis=dict(tickformat='d'), showlegend=False, title_x=0.5)
st.plotly_chart(fig, use_container_width=True)


# delay_at_checkout_in_minutes
fig = px.histogram(data_getaround, x="delay_at_checkout_in_minutes", 
                   title="Répartition du délai de restitutuion d'un véhicule, en minutes.", color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(xaxis_title=None, yaxis_title=None, yaxis=dict(tickformat='d'))
st.plotly_chart(fig, use_container_width=True)

st.markdown("Une valeur négative signifie que le conducteur a restitué le véhicule en avance.")

# state
df_counts = data_getaround["state"].value_counts().reset_index()
df_counts.columns = ["state", "count"]

fig = px.bar(df_counts, x="state", y="count", 
             color="state", title=f"Etat des locations", color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(xaxis_title=None, yaxis_title=None, yaxis=dict(tickformat='d'), showlegend=False, title_x=0.5)
st.plotly_chart(fig, use_container_width=True)


# time_delta_with_previous_rental_in_minutes
fig = px.histogram(data_getaround, x="time_delta_with_previous_rental_in_minutes", 
                   title="Répartition de l'écart entre le début d'une location et la fin de la précédente, en minutes.", nbins=35, 
                   color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(xaxis_title=None, yaxis_title=None, yaxis=dict(tickformat='d'))
st.plotly_chart(fig, use_container_width=True)


st.divider()


## Locations précédentes
st.subheader("Locations pour lesquelles nous avons les informations des locations précédentes")

has_prev = data_getaround['previous_ended_rental_id'].notna()
values = [has_prev.sum(), len(data_getaround) - has_prev.sum()]

fig = px.pie(names=['Avec location précédente', 'Sans location précédente'], values=values, color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig)

percent_prec = has_prev.sum() * 100 / data_getaround.shape[0]

st.markdown(
    f"""
    **Cela représente :** {percent_prec:.2f}% des données. Ces cas sont intéressants à analyser, ce que nous allons faire.  

    ⚠️ *Mais cela reste trop peu pour tirer nos conclusions uniquement sur cet échantillon.*
    """
)
