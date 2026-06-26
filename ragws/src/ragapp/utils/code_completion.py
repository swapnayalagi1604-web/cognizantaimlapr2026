from openai import OpenAI
import os
from dotenv import load_dotenv
#read the OpenAI API key from environment variable
env_path=os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

client = OpenAI(
    api_key=os.getenv("openai_ai_key")
)

response = client.responses.create(
    model="gpt-5",
    input="""
Complete this Python function:

def fibonacci(n):
"""
)

print(response.output_text)