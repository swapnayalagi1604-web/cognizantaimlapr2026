from transformers import AutoTokenizer

model_name = "distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = AutoTokenizer.from_pretrained(
    model_name
)

tokenizer.save_pretrained(
    r"E:\Datascience2026\cognizantaimlapr2026-master\cognizantaimlapr2026-master\ml1\src\resources\hugging-face"
)