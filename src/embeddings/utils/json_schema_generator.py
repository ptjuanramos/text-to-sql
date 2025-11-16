import re
import os
import json
from typing import Any
from src.embeddings.utils.json_formatted_schema import JsonFormattedSchema

class JsonSchemaGenerator:

    def __save_json__(self, obj: dict, output_folder: str):
        """
        Save a JSON object to a file named after obj['name'] in the output folder.
        Returns the filename (for building a master JSON).
        """
        name = obj["name"]
        filename = f"{name}.json"
        filepath = os.path.join(output_folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=4)

        return filename

    def __split_columns__(self, columns_text: str) -> list[str]:
        """
        Split SQL column definitions by commas, ignoring commas inside parentheses.
        """
        columns = []
        current = ""
        parens = 0
        for char in columns_text:
            if char == '(':
                parens += 1
            elif char == ')':
                parens -= 1
            if char == ',' and parens == 0:
                columns.append(current.strip())
                current = ""
            else:
                current += char
        if current:
            columns.append(current.strip())
        return columns

    def __clean_query__(self, query: str) -> str:
        lines = [line.strip() for line in query.splitlines() if line.strip()]
        cleaned_query = " ".join(lines)
        cleaned_query = re.sub(r"\s+", " ", cleaned_query)
        return cleaned_query

    def __parse_to_json__(self, sql_content: str) -> dict[str, str | list[Any] | Any] | None:
        """
        Parse a single CREATE TABLE or CREATE MATERIALIZED VIEW/VIEW statement into a dict,
        including column definitions and foreign key relationships.
        """
        sql_content = sql_content.strip()

        table_match = re.search(
            r"CREATE\s+(?:OR\s+REPLACE\s+)?TABLE\s+(\w+)\s*\((.*)\)\s*;?",
            sql_content,
            re.IGNORECASE | re.DOTALL
        )

        if table_match:
            table_name = table_match.group(1)
            columns_text = table_match.group(2)
            columns = []
            relationships = []

            for col_line in self.__split_columns__(columns_text):
                col_line = col_line.strip()

                if col_line.upper().startswith(("CONSTRAINT", "PRIMARY KEY", "FOREIGN KEY", "UNIQUE")):
                    continue

                col_match = re.match(r"(\w+)\s+(.+)", col_line)
                if col_match:
                    col_name = col_match.group(1)
                    col_type = col_match.group(2).strip()
                    col_type = re.split(r"\s+(NOT NULL|DEFAULT|PRIMARY KEY|UNIQUE)\b",
                                        col_type, flags=re.IGNORECASE)[0].strip()

                    columns.append({
                        "name": col_name,
                        "type": col_type
                    })

                fk_match = re.match(
                    r"FOREIGN KEY\s*\((\w+)\)\s+REFERENCES\s+(\w+)\s*\((\w+)\)",
                    col_line,
                    re.IGNORECASE
                )
                if fk_match:
                    relationships.append({
                        "column": fk_match.group(1),
                        "references_table": fk_match.group(2),
                        "references_column": fk_match.group(3)
                    })

            return {
                "type": "table",
                "name": table_name,
                "columns": columns,
                "relationships": relationships
            }

        view_match = re.match(
            r"CREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+)?VIEW\s+(\w+)\s+(?:.|\s)*?AS\s+(.*)",
            sql_content,
            re.IGNORECASE | re.DOTALL
        )
        if view_match:
            view_name = view_match.group(1)
            query = view_match.group(2).strip()
            query = self.__clean_query__(query)

            view_type = "materialized_view" if re.search(
                r"CREATE\s+(?:OR\s+REPLACE\s+)?MATERIALIZED\s+VIEW",
                sql_content, re.IGNORECASE
            ) else "view"

            return {
                "type": view_type,
                "name": view_name,
                "query": query
            }

        return None

    def generate_schema_file(self, folder_path: str, output_folder: str) -> list[JsonFormattedSchema]:
        """
        Generates the JSON schema file for all sql files within the given folder.

        Table:
        {
            "type": "table",
            "name": table_name,
            "columns": columns,
            "relationships": relationships
        }

        View:
        {
            "type": view_type,
            "name": view_name,
            "query": query
        }
        """
        os.makedirs(output_folder, exist_ok=True)
        json_schemas = []

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".sql"):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    sql_content = f.read()
                    json_result = self.__parse_to_json__(sql_content)

                    if json_result:
                        self.__save_json__(json_result, output_folder)
                        model = JsonFormattedSchema(json_result["type"], json_result, sql_content)
                        json_schemas.append(model)

        return json_schemas