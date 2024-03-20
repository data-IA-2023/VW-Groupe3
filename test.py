from speech_recognition import recognize_from_microphone
from api_meteo import convertisseur_meteo, df_to_date
from utilities import city_to_coordinates
from api_meteo import obtenir_meteo
from nlp import enregistrement_nlp


test=recognize_from_microphone()
print(f"test:{test}")

test2=enregistrement_nlp(test["speech_recognition_result.text"])
print(f"test2:{test2}")


test3=city_to_coordinates(test2["ville"])
print(f"test3:{test3}")


test4=obtenir_meteo(test3["lat"],test3["lon"],test2["date"])
print(f"test4:{test4}")

test5=df_to_date(test2["date"],test4)
print(f"test5:{test5}")

test6=convertisseur_meteo(test5)
print(f"test6:{test6}")