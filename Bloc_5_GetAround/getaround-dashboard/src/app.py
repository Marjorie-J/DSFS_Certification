import streamlit as st
st.set_page_config(layout="wide")

from utils.common import load_data

# Load data
data_getaround = load_data()

pages = [
    st.Page("pages/home.py", title="GetAround Web Dashboard"),
    st.Page("pages/eda.py", title="EDA", icon="📈"),
    st.Page("pages/retards.py", title="Analyse des retards", icon="🕰️"),
    st.Page("pages/enchainement_loc.py", title="Enchainement des locations", icon="⏭️"),
    st.Page("pages/delai.py", title="Délai minimum entre 2 locations", icon="🔬"),
    st.Page("pages/estimation_prix.py", title="Estimation du prix de location", icon="💸")
]

pg = st.navigation(pages)
pg.run()