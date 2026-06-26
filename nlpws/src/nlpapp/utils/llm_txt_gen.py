import os

from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from google import genai
from google.genai.types import GenerateContentConfig
env_path = os.path.join(os.path.dirname(__file__),'..', '.env')
load_dotenv(env_path)

#read anthropic api key from .env file
anthropic_api_key = os.getenv('anthropic_api_key')

client=Anthropic(api_key=anthropic_api_key)

result=client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Tamil Nadu Cheif Minister?"}
    ],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
)

text = "".join(b.text for b in result.content if b.type == "text")
print(text)

#use gemini llm
gemini_api_key=os.getenv("gemini_api_key")
client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Tamil Nadu Chief Minister?",
    config=GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=200,
        top_p=0.9,
        top_k=40
    )
)
print("Gemini response:")
print(response.text)