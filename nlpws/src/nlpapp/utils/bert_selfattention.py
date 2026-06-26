import os
import warnings

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

warnings.filterwarnings("ignore")

from transformers import logging

logging.set_verbosity_error()
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

sentence = "The laptop battery is not charging"

tokenizer = BertTokenizer.from_pretrained(
    "bert-base-uncased"
)

model = BertModel.from_pretrained(
    "bert-base-uncased",
    output_attentions=True
)

inputs = tokenizer(sentence, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

tokens = tokenizer.convert_ids_to_tokens(
    inputs["input_ids"][0]
)

print("Tokens:")
print(tokens)

# First Layer, First Head
attention = outputs.attentions[0][0][0]

print("\nAttention Summary")

for i, token in enumerate(tokens):

    if token in ['[CLS]', '[SEP]']:
        continue

    row = attention[i].numpy().copy()

    # Ignore self-attention
    row[i] = 0

    # Ignore CLS and SEP
    row[0] = 0
    row[-1] = 0

    max_idx = np.argmax(row)

    print(
        f"{token:10} --> {tokens[max_idx]:10} "
        f"Score={row[max_idx]:.3f}"
    )