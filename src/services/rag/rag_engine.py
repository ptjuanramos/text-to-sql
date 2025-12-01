from dotenv import load_dotenv

from src.common.text_to_sql_ai_search import TextToSqlAISearch
from src.common.text_to_sql_completion import TextToSqlCompletion
from src.services.rag.prompt_builder import PromptBuilder

class RagEngine:
    def __init__(self):
        load_dotenv()
        self.ai_search = TextToSqlAISearch()
        self.completion = TextToSqlCompletion()

    def get_query(self, input_text: str):
        embeddings_results = self.ai_search.hybrid_search(input_text)
        prompt = PromptBuilder.build_sql_prompt(input_text, embeddings_results)
        result_query = self.completion.get_query(prompt)
        return result_query