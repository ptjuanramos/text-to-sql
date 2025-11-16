from openai import AzureOpenAI
import json
import os

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01"
)

def embed_table(schema_text):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=schema_text
    )
    return response.data[0].embedding