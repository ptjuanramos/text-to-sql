from typing import List
from openai import AzureOpenAI
import os

class EmbeddingGenerator:

    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_EMBEDDING_MODEL_ENDPOINT"),
            api_key=os.getenv("AZURE_EMBEDDING_KEY"),
            api_version=os.getenv("AZURE_EMBEDDING_MODEL_VERSION")
        )

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
            input=text
        )
        return response.data[0].embedding