from dotenv import load_dotenv
import os, json, re
from src.utils.embeddings.utils.json_formatted_schema import JsonFormattedSchema
from src.common.embeddings_generator import EmbeddingGenerator
from src.common.text_to_sql_ai_search import TextToSqlAISearch

load_dotenv()

embedding_generator = EmbeddingGenerator()

def read_json_schemas() -> list[JsonFormattedSchema]:
    base_dir = os.path.join(".", "schema", "json", "tables")

    schemas = []

    for filename in os.listdir(base_dir):
        json_path = os.path.join(base_dir, filename)

        with open(json_path, "r") as f:
            schema_json = json.load(f)

        if schema_json:
            schema_obj = JsonFormattedSchema(
                schema_type=schema_json.get("type", "unknown"),
                schema_json=schema_json
            )
            schemas.append(schema_obj)

    return schemas

def clean_id(name):
    return re.sub(r'[^a-zA-Z0-9_\-=]', '_', name)


if __name__ == "__main__":
    folder_path = "../schema/sql/tables"
    output_path = "../schema/json/tables"
    json_schemas = read_json_schemas()

    docs = []

    for json_schema in json_schemas:
        doc = {
            "id": clean_id(json_schema.schema_json["name"]),
            "type": json_schema.schema_type,
            "name": json_schema.schema_json["name"],
            "schema_text": json_schema.get_schema_toon(), #TODO need to analyze if TOON will perform better.
            "embedding": json_schema.get_json_schema_embed()
        }

        print(doc)

        docs.append(doc)

        assert isinstance(doc["embedding"], list), "Embedding must be a list"
        assert len(doc["embedding"]) == 1536, "Embedding dimension mismatch"

    text_to_sql_ai_search = TextToSqlAISearch()
    text_to_sql_ai_search.create_index_if_not_exists()

    results = text_to_sql_ai_search.save_schema_documents(docs)
    print(results)

