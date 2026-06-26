import os

from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

env_path = os.path.join(os.path.dirname(__file__),'..', '.env')
load_dotenv(env_path)

#read anthropic api key from .env file
anthropic_api_key = os.getenv('anthropic_api_key')

client=Anthropic(api_key=anthropic_api_key)
while True:
    input_text = input("Enter your question (or 'exit' to quit): ")
    if input_text.lower() == 'exit':
        break
    result=client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": input_text}
        ],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
    )

    text = "".join(b.text for b in result.content if b.type == "text")
    print(text)

