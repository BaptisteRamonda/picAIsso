# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from lib2to3.pygram import python_grammar_no_print_statement
from gtts import gTTS
import pygame
import spacy
import os
import json
from translate import Translator
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher


class ActionTTS(Action):

    def name(self) -> Text:
        return "action_tts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Récupérer le dernier message du système
        bot_event = next(e for e in reversed(tracker.events) if e["event"] == "bot")
        text_from_bot = bot_event['text']

        # Synthétiser la réponse à partir de la chaîne de texte du dernier message du système
        tts = gTTS(text=text_from_bot, lang="fr")
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
    

class ActionTextProcessing(Action):

    def name(self) -> Text:
        return "action_tp"
    

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Récupérer la phrase
        user_event = next(e for e in reversed(tracker.events) if e["event"] == "user")
        phrase = user_event['text']

         # Traduire la phrase
        phrase_traduite = Translator(from_lang="fr", to_lang="en").translate(phrase)

        # Charger le modèle de langue spaCy pour la langue source
        nlp_en = spacy.load(f"en_core_web_sm")

        # Analyser la phrase traduite avec spaCy en anglais
        doc_en = nlp_en(phrase_traduite)

        # Extraire les lemmes des mots-clés (noms propres et autres)
        lemmes = [token.lemma_ for token in doc_en if token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV', 'ADP']] + [token.lemma_ for token in doc_en.ents if token.label_ in ['GPE', 'LOC']]
        while lemmes and nlp_en(lemmes[0])[0].pos_ in ['ADV', 'VERB']:
            lemmes.pop(0)

        # Extraire les slots Type / Theme / Style de RASA
        type_text = tracker.get_slot("type_art")
        theme_text = tracker.get_slot("theme")
        style_text = tracker.get_slot("style")

        # Créer un dictionnaire JSON des mots-clés
        prompt_json = {
                "Type": type_text,
                "Theme": theme_text,
                "Style": style_text,
                "Details": lemmes
            }

        json_str = json.dumps(prompt_json, ensure_ascii=False)

        # Chemin du dossier et du fichier JSON
        dossier = "./json"
        fichier_json = "prompt.json"
        chemin_complet = os.path.join(dossier, fichier_json)

        # Supprimer le fichier JSON s'il existe déjà
        if os.path.exists(chemin_complet):
            os.remove(chemin_complet)

        # Créer le dossier s'il n'existe pas déjà
        if not os.path.exists(dossier):
            os.makedirs(dossier)

        # Enregistrer le fichier JSON
        with open(chemin_complet, 'w') as fichier:
            json.dump(json_str, fichier, indent=2)

        print(f"Le fichier JSON a été enregistré dans : {chemin_complet}")

        return []   
    
class ActionShowImage(Action):

    def name(self) -> Text:
        return "action_si"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Obtenez la valeur du slot "type_art"
        type_art = tracker.get_slot("type_art")

        # Vérifiez si le slot "type_art" est égal à "peinture"
        if type_art and type_art.lower() == "peinture":
            # Appellez l'action "utter_show_painting"
            dispatcher.utter_message(template="utter_show_painting")
        elif type_art and type_art.lower() == "dessin":
            # Appellez l'action "utter_show_painting"
            dispatcher.utter_message(template="utter_show_drawing")
        elif type_art and type_art.lower() == "photo":
            # Appellez l'action "utter_show_painting"
            dispatcher.utter_message(template="utter_show_photography")
        else:
            # Si la condition n'est pas remplie, vous pouvez ajouter une réponse alternative
            dispatcher.utter_message(text="Il semblerait qu'il y ait eu une erreur dans le processus... Et si nous recommencions notre conversation ?")

        return [] 