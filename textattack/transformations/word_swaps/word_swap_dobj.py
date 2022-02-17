# Author: Brahmani Nutakki
# Code to swap the direct object in the hypothesis

"""
Direct Object Word Swap using WordNet
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


class WordSwapDobj(WordSwap):
    """Transforms an input by replacing its words with chosen option from WordNet."""

    def __init__(self, language="eng"):
        if language not in wordnet.langs():
            raise ValueError(f"Language {language} not one of {wordnet.langs()}")
        self.language = language

    def _get_replacement_words(self, word, current_text, random=False):
        # gets replacement words from wordnet based on the choice of --word-replacement
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
        # Only one index is returned.
        nlp = spacy.load("en_core_web_sm")
        premise = str(list(current_text._text_input.values())[0])
        premise_num_words = len(premise.split())
        hypothesis = str(list(current_text._text_input.values())[1])
        # Only hypothesis is perturbed
        text = nlp(hypothesis)
        # incase of multiple sentences, consider the root word in the last sentence
        for s in text.sents:
            root_word = s.root
        try:
            for child in root_word.children:
                if child.dep_ == 'dobj':
                    dobj_word = child.text
                    dobj_index = hypothesis.split().index(dobj_word)
                    break
            temp = premise_num_words + dobj_index
        except Exception:
            temp = -1
        return temp

    def _get_transformations(self, current_text, indices_to_modify):
        transformed_texts = []
        # change to try and except block like in word_swap_root
        indices_to_modify = self._get_index_to_replace(current_text)
        try:
            if indices_to_modify != -1:
                word = current_text.words[indices_to_modify]
                replacement_words = self._get_replacement_words(word, current_text)
                for r in replacement_words:
                    transformed_texts_idx = []
                    if r != wordnet.morphy(word) and textattack.shared.utils.is_one_word(r):
                        if '_' in r:
                            r.replace('_', ' ')
                        transformed_texts_idx.append(
                            current_text.replace_word_at_index(indices_to_modify, r)
                        )
                        transformed_texts.extend(transformed_texts_idx)
        except IndexError as e:
            print(e)

        return transformed_texts
