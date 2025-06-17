import pandas as pd
import random
import streamlit as st

### Config
st.set_page_config(
    page_title="The North Face",
    page_icon="🏔️",
    layout="wide"
)


### App
st.title("The North Face - Recommandations de produits 🏔️")

st.markdown("""
    Bienvenue dans le système de recommandation de produirs de The North Face ! 
            
    Parcourez notre sélection, choisissez un produit qui vous plaît, et découvrez des articles similaires adaptés à vos préférences.
""")

## chargement corpus
DATA_URL = ("../datas/sample-data-clean-clusters.csv")

@st.cache_data
def load_data():
    df = pd.read_csv("../datas/sample-data-clean-clusters.csv", index_col="id")
    return df.sort_index(ascending=True)

df_corpus = load_data()
##


## articles similaires
def find_similar_items(item_id):
    # Item inexistant
    if item_id not in df_corpus.index:
        st.write("Cet item n'existe pas.")
        return []

    cluster_id = df_corpus.loc[item_id, "cluster"]
    
    # Item hors cluster
    if cluster_id == -1:
        st.write("Cet item ne peut pas être rapproché d'un autre item.")
        return []

    # Obtenir tous les items du même cluster, sauf l'item demandé
    mask_same_cluster_items = ((df_corpus["cluster"] == cluster_id) & (df_corpus.index != item_id))
    same_cluster_items = df_corpus[mask_same_cluster_items].index.tolist()

    # Sélectionner 5 items aléatoirement (ou moins si pas assez)
    return random.sample(same_cluster_items, min(5, len(same_cluster_items)))
##


## SELECTION D'UN PRODUIT
# Construire la liste d'affichage : tuples (affichage, id)
corpus = [ (f"{row.name} - {row['description']}", row.name) for _, row in df_corpus.iterrows() ]

# Extraire juste les affichages (pour le selectbox)
corpus_to_display = [corp[0] for corp in corpus]

# SelectBox
selected_product = st.selectbox("Choisir un article",
    corpus_to_display,
    index=None,
    placeholder="Choisir un article ...")
##


## PRODUIT SELECTIONNE
if selected_product != None :
    # Retrouver la description à partir de l'affichage
    selected_id = dict(corpus)[selected_product]
    description = df_corpus.loc[selected_id, "description"]

    # Produit sélectionné
    container_selected = st.container(border=True)
    container_selected.write("Article sélectionné")
    container_selected.write(selected_id)
    container_selected.markdown(description, unsafe_allow_html=True)

    # Produits recommendés
    container_recommended = st.container(border=True)
    container_recommended.write("Articles recommandés")

    for item in find_similar_items(selected_id):
        description = df_corpus.loc[item, "description"]
        container_recommended.write(item)
        container_recommended.markdown(description, unsafe_allow_html=True)
        container_recommended.divider()