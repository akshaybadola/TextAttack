# Author: Brahmani Nutakki
# Code to replce the nominal subject in the hypothesis

"""
not working - nan to integer
NOminal Subnject Word Swap using WordNet
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


class WordSwapNsubj(WordSwap):
    """Transforms an input by replacing its words with Nominal Subject from WordNet."""

    def __init__(self, language="eng"):
        if language not in wordnet.langs():
            raise ValueError(f"Language {language} not one of {wordnet.langs()}")
        self.language = language

    def _get_replacement_words(self, word, random=False):
        # get replacement words from wordnet
        # change code similar to word_swap_root

        temp = 0
        if sys.argv[9] == "synonym":
            temp = get_synonyms(word)
        elif sys.argv[9] == "antonym":
            temp = get_antonyms(word)
        elif sys.argv[9] == "hypernym":
            temp = get_hypernyms(word)
        elif sys.argv[9] == "hyponym":
            temp = get_hyponyms(word)

        return temp

    def _get_index_to_replace(self, current_text):
        # Only one index is returned.
        word_check = 0
        nlp = spacy.load("en_core_web_sm")
        premise = str(list(current_text._text_input.values())[0])
        premise_num_words = len(premise.split())
        hypothesis = str(list(current_text._text_input.values())[1])
        text = nlp(hypothesis)
        # incase of multiple sentences, root word of last sentence is taken
        for s in text.sents:
            root_word = s.root
        for child in root_word.children:
            if child.dep_ == 'dobj':
                nsubj_word = child.text
                nsubj_index = hypothesis.split().index(nsubj_word)
                word_check = 1
                break
        if word_check == 0:
            temp = -1
        else:
            temp = premise_num_words + nsubj_index
        return temp

    def _get_transformations(self, current_text, indices_to_modify):
        transformed_texts = []
        # replace with try and except similar to word_swap_root
        indices_to_modify = self._get_index_to_replace(current_text)
        if indices_to_modify == -1:
            transformed_texts.append(current_text)
        else:
            word = current_text.words[indices_to_modify]
            replacement_words = self._get_replacement_words(word)
            transformed_texts_idx = []
            for r in replacement_words:
                if r != word and textattack.shared.utils.is_one_word(r):
                    transformed_texts_idx.append(
                        current_text.replace_word_at_index(indices_to_modify, r)
                    )
                    transformed_texts.extend(transformed_texts_idx)

        return transformed_texts
