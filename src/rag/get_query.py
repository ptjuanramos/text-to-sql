from dotenv import load_dotenv
import sys

from src.common.text_to_sql_ai_search import TextToSqlAISearch
from src.common.text_to_sql_completion import TextToSqlCompletion
from src.rag.prompt_builder import PromptBuilder


def get_query(input_text: str):
    load_dotenv()
    ai_search = TextToSqlAISearch()
    completion = TextToSqlCompletion()

    embeddings_results = ai_search.hybrid_search(input_text)
    prompt = PromptBuilder.build_sql_prompt(input_text, embeddings_results)
    result_query = completion.get_query(prompt)

    print(f"Input text: {input_text}")
    print(f"Result query: {result_query}")

if __name__ == "__main__":
    text = " ".join(sys.argv[1:])
    get_query("List all customers")
