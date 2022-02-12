import transformers

import textattack

model_path = "../bert-base-uncased-MNLI"

tokenizer = transformers.AutoTokenizer.from_pretrained(model_path)
model = transformers.AutoModelForSequenceClassification.from_pretrained(model_path)

model = textattack.models.wrappers.HuggingFaceModelWrapper(model, tokenizer)
