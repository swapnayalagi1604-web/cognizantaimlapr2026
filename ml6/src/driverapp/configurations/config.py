import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from .env file
load_dotenv(env_path)
RABBITMQ_URL = os.getenv('url')
QUEUE_NAME = os.getenv('queue_name')
