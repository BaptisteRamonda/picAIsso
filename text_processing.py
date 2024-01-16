import spacy
from translate import Translator

# Télécharger et charger le modèle de langue spaCy pour l'anglais
nlp_en = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")

def extraire_mots_cles_en(phrase, src='fr', dest='en'):
    # Traduire la phrase
    phrase_traduite = Translator(from_lang=src, to_lang=dest).translate(phrase)
    print(phrase_traduite)

    # Analyser la phrase traduite avec spaCy en anglais
    doc_en = nlp_en(phrase_traduite)

    # Extraire les lemmes des mots-clés (noms propres et autres)
    lemmes = [token.lemma_ for token in doc_en if token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV', 'ADP']] + [token.lemma_ for token in doc_en.ents if token.label_ in ['GPE', 'LOC']] 
    while lemmes and nlp_en(lemmes[0])[0].pos_ in ['ADV', 'VERB']:
        lemmes.pop(0)
        
    return lemmes

def extraire_mots_cles(phrase):
    # Analyser la phrase traduite avec spaCy en anglais
    doc_fr = nlp_fr(phrase)
    print(phrase)

    # Extraire les lemmes des mots-clés (noms propres et autres)
    lemmes_fr = [token.lemma_ for token in doc_fr if token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV', 'ADP']]

    # Ignorer les mots de liaison et les adverbes au début en français
    while lemmes_fr and nlp_fr(lemmes_fr[0])[0].pos_ in ['ADV', 'VERB']:
        lemmes_fr.pop(0)
    return lemmes_fr

# Exemple d'utilisation
phrase = "Oui, je veux ajouter un astronaute chevauchant un cheval sur Mars"
mots_cles = extraire_mots_cles_en(phrase)
mots_cles_fr = extraire_mots_cles(phrase)
print("Mots-clés extraits en anglais :", mots_cles)
print("Mots-clés extraits en français :", mots_cles_fr)
