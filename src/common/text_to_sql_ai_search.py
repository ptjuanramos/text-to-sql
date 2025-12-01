import os
from typing import Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents._generated.models import IndexingResult
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SearchField,
    SearchFieldDataType
)

INDEX_NAME = "schema-index"
VECTOR_DIM = 1536  # text-embedding-3-small

class TextToSqlAISearch:
    def __init__(self):

        self.index_client = SearchIndexClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        )

        self.search_client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=INDEX_NAME,
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        )

    def hybrid_search(self, text: str) -> list[Any]:
        #embedding_generator = EmbeddingGenerator()
        #input_embed = embedding_generator.embed(text)

        results = self.search_client.search(
            search_text=text,
            # TODO: Needs more research - score, filter, semantics, improve embeddings.
            # vector_queries=[VectorizedQuery(
            #     vector=input_embed,
            #     fields="embedding"
            # )]
        )

        filtered = []
        for r in results:
            score = r.get("@search.score", 0)
            filtered.append({
                "id": r["id"],
                "name": r.get("name"),
                "type": r.get("type"),
                "schema_text": r.get("schema_text"),
                "score": score
            })

        return filtered


    def create_index_if_not_exists(self):
        existing_indexes = list(self.index_client.list_index_names())

        if INDEX_NAME not in existing_indexes:
            vector_algorithm = HnswAlgorithmConfiguration(
                name="my-hnsw-config"
            )

            vector_profile = VectorSearchProfile(
                name="my-vector-profile",
                algorithm_configuration_name="my-hnsw-config"
            )

            vector_search = VectorSearch(
                algorithms=[vector_algorithm],
                profiles=[vector_profile]
            )

            index = SearchIndex(
                name=INDEX_NAME,
                fields=[
                    SimpleField(name="id", type="Edm.String", key=True),
                    SimpleField(name="type", type="Edm.String", filterable=True, sortable=True),
                    SearchableField(name="name", type="Edm.String", searchable=True),
                    SearchableField(name="schema_text", type="Edm.String", searchable=True),
                    SearchField(
                        name="embedding",
                        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        vector_search_dimensions=VECTOR_DIM,
                        vector_search_profile_name="my-vector-profile"
                    ),
                ],
                vector_search=vector_search
            )

            self.index_client.create_index(index)
            print(f"Index '{INDEX_NAME}' created.")
        else:
            print(f"Index '{INDEX_NAME}' already exists.")

    def save_schema_documents(self, schema_documents: list[Dict]) -> list[IndexingResult]:
        return self.search_client.upload_documents(documents=schema_documents)