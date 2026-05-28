import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from .env file
load_dotenv(env_path)

CONSUL_HOST = os.getenv("CONSUL_HOST")
CONSUL_PORT = int(os.getenv("CONSUL_PORT"))