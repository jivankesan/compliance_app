import os

from dotenv import load_dotenv

 

class Config:

    def __init__(self):

        load_dotenv()

        self.model_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        self.model_api_key = os.getenv("AZURE_OPENAI_API_KEY")

        self.model_generate = os.getenv("AZURE_MODEL_NAME")

        self.model_embed = os.getenv("AZURE_EMBEDMODEL_NAME")

        self.deployment = os.getenv("AZURE_MODEL_NAME")

        self.api_version = "2024-06-01"