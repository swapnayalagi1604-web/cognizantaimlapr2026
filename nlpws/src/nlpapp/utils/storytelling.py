from openai import OpenAI
from dotenv import load_dotenv
import os
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

client = OpenAI(api_key=os.getenv("openai_api_key"))

prompt = """
Write a short story for children.

Theme: Courage
Main character: Meena, a shy girl
Setting: School annual day
Conflict: She is afraid to speak on stage
Ending: She becomes confident
Moral: Believe in yourself
"""
#temperature controls the creativity of the output, 
# higher values like 0.8 will make the output more creative, 
# while lower values like 0.2 will make it more focused and deterministic.
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a creative story writer."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.8,
    max_tokens=700
)

print(response.choices[0].message.content)