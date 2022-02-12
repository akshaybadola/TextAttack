# Author: Brahmani Nutakki
# Code to load mnli dataset locally

import textattack
import contractions
import json
import string


# remove contractions
def decontract(text):
    return contractions.fix(text)


# remove punctutations
def remove_punctuation(text):
    text = "".join([i for i in text if i not in string.punctuation])
    return text


data = []
dataset = []
with open('./resources/multinli_1.0_dev_matched.jsonl', 'r') as fp:
    for line in fp:
        data.append(json.loads(line))

for row in data:
    temp1 = ()
    temp3 = ()

    temp1 = (remove_punctuation(decontract(row["sentence1"])),
             remove_punctuation(decontract(row["sentence2"])))
    # labels as per glue datset
    if row["gold_label"] == "entailment":
        temp2 = 0
    elif row["gold_label"] == "neutral":
        temp2 = 1
    elif row["gold_label"] == "contradiction":
        temp2 = 2
    temp3 = (temp1, temp2)
    dataset.append(tuple(temp3))

# label_map to map labels as per textattack
dataset = textattack.datasets.Dataset(dataset, input_columns=("premise", "hypothesis"),
                                      label_names=("entailment", "neutral", "contradiction"),
                                      label_map={0: 1, 1: 2, 2: 0})
