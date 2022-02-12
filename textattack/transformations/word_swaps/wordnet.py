# Author: Brahmani Nutakki
# Wordnet functions to retrieve replacement words

"""
Get replacement words from wordnet

"""

from nltk.corpus import wordnet
from nltk.wsd import lesk
import spacy


def get_synonyms(word, current_text):
    synonyms = set()
    # get synset with the nearest sense based on the text and sentence
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(list(current_text._text_input.values())[1])
    for token in doc:
        if token.text == word:
            pos = token.pos_
            break
    try:
        near_synset = lesk(list(current_text._text_input.values())[1], word, pos.lower()[0])
        # get the words with the same sense as the synset i.e the lemmas
        for lem in near_synset.lemmas():
            synonyms.add(lem.name())
    except Exception:
        # dummy line for exception
        pos = 0
        # print("No synonym found with the same sense")
        # synonyms.add(word)

    return list(synonyms)


def get_antonyms(word):
    antonyms = set()
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            if lem.antonyms() and lem.antonyms()[0].name() != word:
                antonyms.add(lem.antonyms()[0].name())

    return list(antonyms)


def get_hypernyms(word):
    hypernyms = set()
    for syn in wordnet.synsets(word):
        for s in syn.hypernyms():
            if s.name().split(',')[0] != word:
                hypernyms.add(s.name().split('.')[0])

    return list(hypernyms)


def get_hyponyms(word):
    hyponyms = set()
    for syn in wordnet.synsets(word):
        for s in syn.hyponyms():
            if s.name().split(',')[0] != word:
                hyponyms.add(s.name().split('.')[0])

    return list(hyponyms)
