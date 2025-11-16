from typing import List
from openai import AzureOpenAI
import os

class EmbeddingGenerator:

    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01"
        )

    def embed_single_schema(self, schema_text: str) -> List[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=schema_text
        )
        return response.data[0].embedding