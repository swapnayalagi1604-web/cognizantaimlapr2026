import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

LOAN_FILE_PATH = os.getenv('loan_file_path')
MODEL_FILE_PATH = os.getenv('model_file_path')