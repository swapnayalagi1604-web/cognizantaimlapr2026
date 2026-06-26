import os
from dotenv import load_dotenv
from openai import OpenAI
env_path = os.path.join(os.path.dirname(__file__), '..', ".env")
load_dotenv(env_path)

endpoint = os.getenv("azure_openai_project_endpoint")
api_key = os.getenv("azure_key")

print("Endpoint:", endpoint)
print("API key loaded:", api_key is not None)

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

speech = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="nova",
    input="""
    மார்கழித் திங்கள்
    மதிநிறைந்த நன்னாளால்
    நீராடப் போதுவீர்
    போதுமினோ நேரிழையீர்
    """
)

speech.stream_to_file("tamil_song.mp3")

print("MP3 generated successfully")