import os
import pyodbc
from dotenv import load_dotenv
from collections import defaultdict
import json

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "1433")

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={DB_HOST},{DB_PORT};DATABASE={DB_NAME};"
    f"UID={DB_USER};PWD={DB_PASS};Encrypt=no;"
)

db_connection = pyodbc.connect(conn_str)
query = """
SELECT 
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    t.TABLE_TYPE,
    c.COLUMN_NAME,
    c.ORDINAL_POSITION,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.NUMERIC_PRECISION,
    c.NUMERIC_SCALE,
    c.IS_NULLABLE,
    c.COLUMN_DEFAULT,

    CASE WHEN pk.COLUMN_NAME IS NOT NULL THEN 1 ELSE 0 END AS IS_PRIMARY_KEY,

    fk.FK_NAME AS FOREIGN_KEY_NAME,
    fk.REFERENCED_TABLE_SCHEMA,
    fk.REFERENCED_TABLE_NAME,
    fk.REFERENCED_COLUMN_NAME,

    sm.definition AS VIEW_DEFINITION
FROM 
    INFORMATION_SCHEMA.TABLES t
INNER JOIN 
    INFORMATION_SCHEMA.COLUMNS c 
        ON t.TABLE_SCHEMA = c.TABLE_SCHEMA
       AND t.TABLE_NAME = c.TABLE_NAME

LEFT JOIN (
        SELECT 
            ku.TABLE_SCHEMA,
            ku.TABLE_NAME,
            ku.COLUMN_NAME
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
        INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku
            ON tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
        WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
) pk
    ON c.TABLE_SCHEMA = pk.TABLE_SCHEMA
   AND c.TABLE_NAME = pk.TABLE_NAME
   AND c.COLUMN_NAME = pk.COLUMN_NAME

LEFT JOIN (
        SELECT
            ku.TABLE_SCHEMA,
            ku.TABLE_NAME,
            ku.COLUMN_NAME,
            rc.CONSTRAINT_NAME AS FK_NAME,
            pk.TABLE_SCHEMA AS REFERENCED_TABLE_SCHEMA,
            pk.TABLE_NAME AS REFERENCED_TABLE_NAME,
            pk.COLUMN_NAME AS REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
        INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku
            ON rc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
        INNER JOIN (
            SELECT 
                ku2.CONSTRAINT_NAME,
                ku2.TABLE_SCHEMA,
                ku2.TABLE_NAME,
                ku2.COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku2
        ) pk
            ON rc.UNIQUE_CONSTRAINT_NAME = pk.CONSTRAINT_NAME
) fk
    ON c.TABLE_SCHEMA = fk.TABLE_SCHEMA
   AND c.TABLE_NAME = fk.TABLE_NAME
   AND c.COLUMN_NAME = fk.COLUMN_NAME

LEFT JOIN sys.objects o
    ON o.name = t.TABLE_NAME
   AND o.schema_id = SCHEMA_ID(t.TABLE_SCHEMA)
   AND o.type = 'V'         -- VIEW

LEFT JOIN sys.sql_modules sm
    ON sm.object_id = o.object_id

WHERE 
    t.TABLE_TYPE IN ('BASE TABLE','VIEW')
ORDER BY 
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    c.ORDINAL_POSITION;
"""

cursor = db_connection.cursor()
cursor.execute(query)
rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]
result = [dict(zip(columns, row)) for row in rows]
db_connection.close()

tables = defaultdict(lambda: {
    "type": None,
    "name": None,
    "query": None,
    "columns": [],
    "primary_keys": [],
    "relationships": []
})

for row in result:
    table_full_name = f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"
    table = tables[table_full_name]

    # TABLE / VIEW / OTHER TYPE
    sql_type = "TABLE" if row["TABLE_TYPE"] == "BASE TABLE" else row["TABLE_TYPE"]
    table["name"] = table_full_name

    # === NEW: store view SQL if available ===
    if row.get("VIEW_DEFINITION"):
        clean_query = row["VIEW_DEFINITION"].replace('\r\n', ' ').replace('\r', ' ')
        table["query"] = clean_query

    # Columns
    column = {
        "name": row["COLUMN_NAME"],
        "type": row["DATA_TYPE"],
        "nullable": row["IS_NULLABLE"]
    }
    table["columns"].append(column)

    # Primary keys
    if row["IS_PRIMARY_KEY"] == 1:
        table["primary_keys"].append(row["COLUMN_NAME"])

    # Foreign keys
    if row["FOREIGN_KEY_NAME"]:
        table["relationships"].append({
            "fk_column": row["COLUMN_NAME"],
            "ref_table": f"{row['REFERENCED_TABLE_SCHEMA']}.{row['REFERENCED_TABLE_NAME']}",
            "ref_column": row["REFERENCED_COLUMN_NAME"]
        })


output_dir = os.path.join(".", "schema", "json", "tables")
os.makedirs(output_dir, exist_ok=True)

for table_name, table_data in tables.items():
    short_name = table_name.split(".")[-1]  # Ex: dbo.customers → customers.json
    file_path = os.path.join(output_dir, f"{short_name}.json")

    with open(file_path, "w") as f:
        json.dump(table_data, f, indent=2)

print(f"Created {len(tables)} schema files in {output_dir}/")