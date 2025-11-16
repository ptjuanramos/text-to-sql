from json_schema_generator import JsonSchemaGenerator

jsonSchemaGenerator = JsonSchemaGenerator()

if __name__ == "__main__":
    folder_path = "../schema/sql/tables"
    output_path = "../schema/json/tables"
    jsonSchemaGenerator.generate_schema_file(folder_path, output_path)