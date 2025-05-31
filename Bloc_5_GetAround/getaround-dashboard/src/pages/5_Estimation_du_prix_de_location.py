import requests
import streamlit as st

st.set_page_config(page_title="GetAround Web Dashboard 🚗", layout="wide")

from utils.common import data_getaround, plot_checkin_thresholds

st.markdown("# Estimation du prix de location 💸")


st.markdown("""
    ### Estimation du prix de location

    Cette section permet d'estimer le **prix de location par jour** de votre véhicule.
    """)


# Création du formulaire

options_bool = {
    "Oui": "True",
    "Non": "False"
}

options_energie = {
    "Diesel": "diesel",
    "Hybride": "hybrid_petrol",
    "Essence": "petrol"
}

options_couleur = {
    "Argent": "silver",
    "Beige": "beige",
    "Blanc": "white",
    "Bleu": "blue",
    "Gris": "grey",
    "Marron": "brown",
    "Noir": "black",
    "Orange": "orange",
    "Rouge": "red",
    "Vert": "green"
}

options_type = {
    "Cabriolet": "convertible",
    "Coupé": "coupe",
    "Break": "estate",
    "Citadine": "hatchback",
    "Berline": "sedan",
    "Mini-Citadine": "subcompact",
    "SUV": "suv",
    "Van": "van"
}



with st.form("rental_price_predict"):

    model = st.selectbox("Modèle", ("Alfa Romeo", "Audi", "BMW", "Citroën", "Ferrari", "Fiat",
                                      "Ford", "Honda", "KIA Motors", "Lamborghini", "Lexus", "Maserati",
                                      "Mazda", "Mercedes", "Mini", "Mitsubishi", "Nissan", "Opel",
                                      "Peugeot", "PGO", "Porsche", "Renault", "SEAT", "Subaru",
                                      "Suzuki", "Toyota", "Volkswagen", "Yamaha"),
                        index=None, placeholder="Modèle")
    
    milage = st.slider("Kilométrage", min_value=0, max_value=600000, value=100000, step=100)

    engine_power = st.slider("Puissance", min_value=0, max_value=500, value=120, step=5)

    fuel = st.selectbox("Energie", list(options_energie.keys()),
                        index=None, placeholder="Energie")

    paint_color = st.selectbox("Couleur", list(options_couleur.keys()),
                        index=None, placeholder="Couleur")

    type = st.selectbox("Type", list(options_type.keys()),
                        index=None, placeholder="Type")

    private_parking = st.selectbox("Parking privé", list(options_bool.keys()),
                        index=None, placeholder="Parking privé")

    gps = st.selectbox("GPS", list(options_bool.keys()),
                        index=None, placeholder="GPS")

    air_conditioning = st.selectbox("Air conditionné", list(options_bool.keys()),
                        index=None, placeholder="Air conditionné")

    automatic = st.selectbox("Automatique", list(options_bool.keys()),
                        index=None, placeholder="Automatique")

    getaround_connect = st.selectbox("Equipement GetAround Connect", list(options_bool.keys()),
                        index=None, placeholder="Equipement GetAround Connect")

    speed_regulator = st.selectbox("Régulateur de vitesse", list(options_bool.keys()),
                        index=None, placeholder="Régulateur de vitesse")

    winter_tires = st.selectbox("Pneus Hiver", list(options_bool.keys()),
                        index=None, placeholder="Pneus Hiver")


    # Bouton pour soumettre le formulaire
    submitted = st.form_submit_button("Estimer")

    # Traitement après la soumission
    if submitted:
        if not model or not milage or not engine_power or not fuel or not paint_color or not \
        type or not private_parking or not gps or not air_conditioning or not automatic or not \
        getaround_connect or not speed_regulator or not winter_tires:
            st.error("Veuillez remplir tous les champs.")
        else:

            payload = {
                "model_key": model,
                "mileage": milage,
                "engine_power": engine_power,
                "fuel":options_energie[fuel], 
                "paint_color": options_couleur[paint_color],
                "car_type": options_type[type],
                "private_parking_available": options_bool[private_parking],
                "has_gps": options_bool[gps],
                "has_air_conditioning": options_bool[air_conditioning],
                "automatic_car": options_bool[automatic],
                "has_getaround_connect": options_bool[getaround_connect],
                "has_speed_regulator": options_bool[speed_regulator],
                "winter_tires": options_bool[winter_tires]
            }

            r = requests.post("https://marjg-getaround-api.hf.space/predict", json=payload)
            response = r.json()

            st.text(f"Estimation de location : {round(response['prediction'], 2)} $ par jour.")