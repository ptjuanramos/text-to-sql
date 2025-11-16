import os

from dotenv import load_dotenv

from src.utils.json_schema_generator import JsonSchemaGenerator
from src.utils.embeddings_generator import EmbeddingGenerator
from src.utils.text_to_sql_ai_search import TextToSqlAISearch

load_dotenv()

json_schema_generator = JsonSchemaGenerator()
embedding_generator = EmbeddingGenerator()

if __name__ == "__main__":
    folder_path = "../schema/sql/tables"
    output_path = "../schema/json/tables"
    json_schemas = json_schema_generator.generate_schema_file(folder_path, output_path)

    docs = []

    # for key, value in os.environ.items():
    #     print(f"{key}={value}")

    for json_schema in json_schemas:
        doc = {
            "id": json_schema.schema_json["name"],
            "type": json_schema.schema_type,
            "name": json_schema.schema_json["name"],
            "schema_text": json_schema.get_schema_text(),
            "embedding": json_schema.get_json_schema_embed()
        }

        docs.append(doc)

        assert isinstance(doc["embedding"], list), "Embedding must be a list"
        assert len(doc["embedding"]) == 1536, "Embedding dimension mismatch"

    text_to_sql_ai_search = TextToSqlAISearch()
    text_to_sql_ai_search.create_index_if_not_exists()

    results = text_to_sql_ai_search.save_schema_documents(docs)
    print(results)

