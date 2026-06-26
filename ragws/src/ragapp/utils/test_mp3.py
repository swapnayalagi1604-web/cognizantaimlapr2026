from openai import OpenAI
import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '..', ".env")
load_dotenv(env_path)

client = OpenAI(
    base_url=os.getenv("azure_openai_project_endpoint"),
    api_key=os.getenv("azure_key")
)

with open("test_audio.mp3", "rb") as f:
    response = client.audio.transcriptions.create(
        model="transcribe",
        file=f
    )

print(response)