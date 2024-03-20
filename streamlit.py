import streamlit as st
from nlp import enregistrement_nlp
from speech_recognition import recognize_from_microphone
from api_meteo import convertisseur_meteo, df_to_date
from utilities import city_to_coordinates
from api_meteo import obtenir_meteo

# Afficher une image neutre par défaut
st.image("meteo.jpeg", use_column_width=True)

st.write("""
<div style='text-align:center'>
    <h1>Météo par reconnaissance vocale</h1>

</div>
""", unsafe_allow_html=True)

# Définir une variable de drapeau pour indiquer si le bouton a été pressé
bouton_presse = False

# Centrer le bouton horizontalement
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    message_enregistrement = st.empty()
    if st.button("Appuyez ici et faite votre demande", key="record_button"):
        bouton_presse = True
        message_enregistrement.info("Enregistrement en cours...",icon="⏺️")

        # Reconnaissance vocale et traitement des données
        test = recognize_from_microphone()
        test2 = enregistrement_nlp(test["speech_recognition_result.text"])
        test3 = city_to_coordinates(test2["ville"])
        test4 = obtenir_meteo(test3["lat"], test3["lon"], test2["date"])
        test5 = df_to_date(test2["date"], test4)
        test6 = convertisseur_meteo(test5["df"])

        # Affichage de l'image en fonction de test6
        if test6 == "Il fait beau":
            st.image("soleil.jpg", width=300)
        elif test6 == "Un peu de pluie":
            st.image("pluie.jpeg", width=300)
        elif test6 == "Beaucoup de pluie":
            st.image("beaucouppluie.jpeg", width=300)

    
# Affichage des résultats uniquement lorsque le bouton est pressé
if bouton_presse:
    message_enregistrement.empty()
    st.write("Votre demande:", test["format"])
    st.write("Ville:", test2["ville"])
    st.write("Date:", test5["date"])
    st.write("Prévision météo:", test6)
    st.write("Température minimum:", test5["temperaturemin"],"˚C")
    st.write("Température maximum:", test5["temperaturemax"],"˚C")
    st.write("Jours suivants", test4)
    

