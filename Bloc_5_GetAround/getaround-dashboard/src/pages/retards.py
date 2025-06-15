import plotly.express as px
import streamlit as st

from utils.common import load_data


st.markdown("# Analyse des retards 🕰️")


# Load data
data_getaround = load_data()

## Fréquence des retards
st.subheader("A quelle fréquence les conducteurs rendent-il les véhicules en retard ?")

# Calcul des valeurs
total_delay_checkout = data_getaround["delay_at_checkout_in_minutes"].notnull().sum()
en_retard = (data_getaround["delay_at_checkout_in_minutes"] > 0).sum()
en_avance = (data_getaround["delay_at_checkout_in_minutes"] < 0).sum()
a_l_heure = (data_getaround["delay_at_checkout_in_minutes"] == 0).sum()

labels = ['En avance', 'À l’heure', 'En retard']
sizes = [en_avance, a_l_heure, en_retard]

fig = px.pie(values=sizes, names=labels, color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)



# Impact sur la location suivante
st.subheader("Concernant les retards, quel impact cela a sur la prochaine location ?")

late_and_canceled = data_getaround[(data_getaround["previous_delay_at_checkout_in_minutes"] > 0) & (data_getaround["state"] == "canceled")].shape[0]
late_and_not_canceled = data_getaround[(data_getaround["previous_delay_at_checkout_in_minutes"] > 0) & (data_getaround["state"] == "ended")].shape[0]

late_labels = ["Location suivante annulée", "Location suivante maintenue"]
late_sizes = [late_and_canceled, late_and_not_canceled]

fig = px.pie(values=late_sizes, names=late_labels, color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig, use_container_width=True)



# Impact sur la location suivante
st.subheader("Comment les retards sont-ils répartis selon le type de check-in ?")

# Retards moyens par type
fig = px.box(data_getaround, x="checkin_type", y="delay_at_checkout_in_minutes", 
             color="checkin_type", color_discrete_sequence=px.colors.qualitative.Pastel, 
             labels={"checkin_type": "Type de check-in", "delay_at_checkout_in_minutes": "Délai de retour (en minutes)"})
st.plotly_chart(fig)

st.markdown("""
            Pour rappel une valeur négative signifie que le conducteur a restitué le véhicule en avance.

            On observe donc plus de retards au retour pour les location `mobile`.
            """)