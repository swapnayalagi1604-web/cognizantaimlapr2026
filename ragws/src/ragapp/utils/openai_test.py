from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
#must login using az login before running this code
import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__),'..', ".env")
load_dotenv(env_path)
deployment_name = "gpt-4.1-mini"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url=os.getenv("azure_openai_project_endpoint"),
    api_key=token_provider
)

response = client.responses.create(
    model=deployment_name,
    input="What is the capital of France?",
)

print(f"answer: {response.output[0]}")