class PromptBuilder:

    def get_tables_columns_prompt(retrieved: list):
        result = ""
        for table in retrieved:
            cols = ", ".join(table.get("columns", []))
            result += f"- {table['name']} ({cols})\n"

        return result

    def build_sql_prompt(user_query: str, retrieved: list) -> str:
        tables_columns = PromptBuilder.get_tables_columns_prompt(retrieved)
        prompt = f"""
        You are expert in SQL Server DB. Use ONLY the following tables and columns below:
          {tables_columns}
          
        Write correct SQL for the user's request: {user_query}
    
          Rules:
          - Generate ONLY SQL
          - Must run in SQL Server / Azure SQL
          - Do not invent tables or columns
          - Do not include Markdown
          - Only use the tables and columns listed above.
        """

        return prompt