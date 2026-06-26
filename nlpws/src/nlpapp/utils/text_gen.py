#read the hr policy txt file and summarize using encoder decoder model

import os

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__),'..', '.env')

load_dotenv(env_path)

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#read the file

def read_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def encoder_decoder_summarize(text):
    model_name = "t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=5., num_beams=2)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

if __name__ == "__main__":
    file_path = os.getenv('file_path')
    text = read_file(file_path)
    summary = encoder_decoder_summarize(text)
    print(summary)