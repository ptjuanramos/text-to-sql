import json
from typing import Any
#from toon import encode
from src.common.embeddings_generator import EmbeddingGenerator

class JsonFormattedSchema:

    def __init__(self, schema_type: str, schema_json: dict[str, str | list[Any] | Any], sql_schema: str):
        self.schema_type = schema_type
        self.schema_json = schema_json
        self.sql_schema = sql_schema

    def get_json_schema_embed(self):
        embedding_generator = EmbeddingGenerator()
        json_schema_str = json.dumps(self.schema_json)
        return embedding_generator.embed(json_schema_str)

    # def get_schema_toon(self) -> str:
    #     return encode(self.schema_json)

    def get_schema_text(self) -> str:
        schema_type = self.schema_json.get("type", "unknown")
        name = self.schema_json.get("name", "UNKNOWN")
        text = f"{schema_type.title()}: {name}\n"

        if schema_type == "table":
            text += "Columns:\n"
            for col in self.schema_json.get("columns", []):
                text += f"- {col['name']} {col.get('type','UNKNOWN')} nullable={col.get('nullable', True)} pk={col.get('pk', False)}\n"

            for rel in self.schema_json.get("relationships", []):
                text += f"Relationship: {rel.get('from_column')} -> {rel.get('to_table')}.{rel.get('to_column')}\n"

        elif schema_type == "view":
            text += "Query:\n"
            query = self.schema_json.get("query", "")
            text += query + "\n"

        else:
            text = None

        return text
