class PromptBuilder:
    def build_sql_prompt(user_query: str, retrieved: list) -> str:
        prompt = "You are an expert in Oracle DB that generates SQL queries.\n"
        prompt += "Here are the tables and columns available:\n"

        for table in retrieved:
            cols = ", ".join(table.get("columns", []))
            prompt += f"- {table['name']} ({cols})\n"

        prompt += "\nInstructions:\n"
        prompt += "- Only use the tables and columns listed above.\n"
        prompt += "- Write correct SQL for the user's request.\n"
        prompt += "- If aggregation is needed, use standard SQL.\n"
        prompt += "- Use JOINs if necessary.\n\n"

        prompt += f"User request: {user_query}\n"
        prompt += "Generate SQL query:"

        return prompt