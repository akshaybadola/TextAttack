# Author: Brahmani Nutakki
# Code to replace all word of hypothesis using wordnet

"""
All Word Swap using WordNet
==========================================================
"""

import spacy
from nltk.corpus import wordnet
import textattack
from .word_swap import WordSwap
from .wordnet import get_synonyms
from .wordnet import get_antonyms
from .wordnet import get_hypernyms
from .wordnet import get_hyponyms
import sys


class WordSwapAll(WordSwap):
    """Transforms an input by replacing its words with Root Word from WordNet."""

    def __init__(self, language="eng"):
        if language not in wordnet.langs():
            raise ValueError(f"Language {language} not one of {wordnet.langs()}")
        self.language = language

    def _get_replacement_words(self, word, current_text, random=False):
        # get replacement words from Wordnet
        temp = 0
        temp = sys.argv[sys.argv.index("--word-replacement-choice") + 1]

        if temp == "synonym":
            temp = get_synonyms(word, current_text)
        elif temp == "antonym":
            temp = get_antonyms(word)
        elif temp == "hypernym":
            temp = get_hypernyms(word)
        elif temp == "hyponym":
            temp = get_hyponyms(word)
        return temp

    def _get_index_to_replace(self, current_text):
        indices_to_modify = []
        pos_list = ["ADJ", "ADV", "AUX", "INTJ", "NOUN", "NUM", "PROPN", "VERB"]
        nlp = spacy.load("en_core_web_sm")
        premise = str(list(current_text._text_input.values())[0])
        premise_num_words = len(premise.split())
        hypothesis = str(list(current_text._text_input.values())[1])
        text = nlp(hypothesis)
        for sent in text.sents:
            for word in sent:
                if word.pos_ in pos_list:
                    try:
                        indices_to_modify.append(premise_num_words + hypothesis.split().index(word.text))
                    except Exception as e:
                        print(e)

        return indices_to_modify

    def _get_transformations(self, current_text, indices_to_modify):
        # import ipdb; ipdb.set_trace()
        transformed_texts = []
        indices_to_modify = self._get_index_to_replace(current_text)
        for i in indices_to_modify:
            try:
                word = current_text.words[i]
                replacement_words = self._get_replacement_words(word, current_text)
                for r in replacement_words:
                    transformed_texts_idx = []
                    if r != wordnet.morphy(word) and textattack.shared.utils.is_one_word(r):
                        if '_' in r:
                            r.replace('_', ' ')
                        transformed_texts_idx.append(current_text.replace_word_at_index(i, r))
                        transformed_texts.extend(transformed_texts_idx)
                    # if only replacement wprd is synonym
                    elif r == wordnet.morphy(word) and len(replacement_words) == 1:
                        transformed_texts = []

            except IndexError as e:
                print(e)

        return list(set(transformed_texts))
