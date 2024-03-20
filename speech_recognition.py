# Importez les modules requis
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Chargez les variables d'environnement à partir du fichier .env
load_dotenv()

# Définissez la fonction de reconnaissance vocale
def recognize_from_microphone():
    # Configurez les paramètres de la reconnaissance vocale avec les clés d'abonnement et la région
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language = "fr-FR"

    # Configurez le microphone comme source audio par défaut
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Créez un objet SpeechRecognizer pour reconnaître la parole une fois
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Lancez la reconnaissance vocale et attendez le résultat
    print("Veuillez parler :")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # Traitez le résultat de la reconnaissance vocale
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        format=("{}".format(speech_recognition_result.text))
        return {"speech_recognition_result.text":speech_recognition_result.text,"format":format}
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
