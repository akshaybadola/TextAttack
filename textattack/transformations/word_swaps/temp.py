# Author: Brahmani Nutakki
# Temporary file to try libraries

import spacy
import pyinflect
from nltk.wsd import lesk
from nltk.corpus import wordnet

# text1 = "Prototyping, for example, may act as part of the requirements definition process, helping the agency identify and control areas of high uncertainty and technical risk."
# doc = "Prototyping is not important, testing with the actual finished product is better."
# doc = "I am not sure they are old enough to have back packs"
# doc = "There is no road between Esna and Luxor"
doc = "Everyone really hated the newest benefits "
# doc = "Conspiracy theorists believe Mastercard is working on a chip to store all your personal data"
# doc = "Most of Mrinal Sen's work can be found in European collections"
# print(len(doc.split()))
orig = doc
nlp = spacy.load("en_core_web_sm")
doc = nlp(doc)
print(f"Doc: {doc}")
for sent in doc.sents:
    for word in sent:
        print(f"{word}, pos:{word.pos_}, tag:{word.tag_}")
"""
# Shpuld change this to get without iterating
for s in doc.sents:
    t = s.root
l = nlp("is")[0]
print(f"Root: {t.text}")
print(f"pos of likes: {t.tag_}")
print(f"pos of is: {l.tag_}")
print(f"pos of likes: {t.pos_}")
print(f"pos of is: {l.pos_}")
near_synset = lesk(doc, t.text)
synonyms = set()
for lem in near_synset.lemmas():
    print(nlp(lem.name())[0]._.inflect(t.tag_))
    synonyms.add(lem.name())
print(synonyms)
#print(wordnet.synsets(t.text, pos=wordnet.VERB))
# for child in t.children:
    # if child.dep_ == 'dobj':
        # print("ngn")
    # if child.dep_ == 'nsubj':
        # l = child

# Hypernyms
# hypernyms = set()
# for syn in wordnet.synsets('lot'):
    # for s in syn.hypernyms():
        # hypernyms.add(s.name().split('.')[0])

# print(hypernyms)
#blah = lesk(orig, 'likes')
#print(f"lesk synset: {blah}")
#for x in blah.lemmas():
    #print(wordnet.morphy(x.name()), wordnet.morphy(t.text))
    #if (wordnet.morphy(x.name())) == wordnet.morphy(t.text):
        #word = x.name()
        #sense = x.key().split('%')[1]
        #print(word,sense)
        #break
#for x in wordnet.synsets(str(t), pos=t.pos_):
    #for syn in x.lemmas():
        #if syn.name() != word and sense == syn.key().split('%')[1]:
            #print(f"final: {syn.name()}")

"""
