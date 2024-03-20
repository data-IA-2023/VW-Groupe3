from geopy.geocoders import Nominatim
from speech_recognition import recognize_from_microphone
from nlp import enregistrement_nlp


def city_to_coordinates(ville_retranscription):
    ville = enregistrement_nlp(ville_retranscription)["ville"]
    print(ville)
    geolocator = Nominatim(user_agent="vocal_weather_app")
    
    # Send the user' city to geocode service
    location = geolocator.geocode(ville)
    
    # Extract desired data : coordinates
    if location:
        lat = location.latitude
        lon = location.longitude
        print(f'Latitude, Longitude: {lat}, {lon}')
        return {"lat":lat, "lon":lon}
    else:
        print("Ville non trouvée.")
        return None, None
