# Author: Brahmani Nutakki
# Code to replace root word of hypothesis using wordnet

"""
Root Word Swap using WordNet
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


# synonyms.add(syn_word.name())
class WordSwapRoot(WordSwap):
    """Transforms an input by replacing its words with Root Word from WordNet."""

    def __init__(self, language="eng"):
        if language not in wordnet.langs():
            raise ValueError(f"Language {language} not one of {wordnet.langs()}")
        self.language = language

    def _get_replacement_words(self, word, current_text, random=False):
        # get replacement words from Wordnet
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
        text = nlp(hypothesis)
        # incase of mutliple sentences, consider root word of last sentence
        for s in text.sents:
            root_index = s.root.i
        return (premise_num_words + root_index)

    def _get_transformations(self, current_text, indices_to_modify):
        transformed_texts = []
        indices_to_modify = self._get_index_to_replace(current_text)
        try:
            word = current_text.words[indices_to_modify]
            replacement_words = self._get_replacement_words(word, current_text)
            for r in replacement_words:
                transformed_texts_idx = []
                if r != wordnet.morphy(word) and textattack.shared.utils.is_one_word(r):
                    if '_' in r:
                        r.replace('_', ' ')
                    transformed_texts_idx.append(current_text.replace_word_at_index(indices_to_modify, r))
                    transformed_texts.extend(transformed_texts_idx)
                # if only replacement wprd is synonym
                elif r == wordnet.morphy(word) and len(replacement_words) == 1:
                    transformed_texts = []

        except IndexError:
            word = 0
            # print(e)
            # transformed_texts.append(current_text)

        return list(set(transformed_texts))
