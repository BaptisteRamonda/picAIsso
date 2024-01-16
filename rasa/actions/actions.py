# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from gtts import gTTS
import pygame
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionTTS(Action):

    def name(self) -> Text:
        return "action_tts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Récupérer le dernier message du système
        last_bot_message = str(tracker.latest_message['text'])

        # Synthétiser la réponse à partir de la chaîne de texte du dernier message du système
        tts = gTTS(text=last_bot_message, lang="fr")
        tts.save("response.mp3")

        # Initialiser Pygame pour la lecture audio
        pygame.init()
        pygame.mixer.init()

        # Lire le fichier mp3 contenant la réponse
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()

        # Attendre la fin de la lecture audio
        while pygame.mixer.music.get_busy():
            continue

        pygame.quit()

        return []
