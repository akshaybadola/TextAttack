# Author: Brahmani Nutakki
# Code to load mnli from Hugging Face Dataset Repository

import textattack

dataset = textattack.datasets.HuggingFaceDataset("glue", "mnli", "validation_matched", None, {0: 1, 1: 2, 2: 0})
