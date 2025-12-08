import os
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionUserMessageParam


class TextToSqlCompletion:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_VERSION")
        )

    def get_query(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=os.getenv("AZURE_LLM_DEPLOYMENT_NAME"),
            messages=[
                ChatCompletionUserMessageParam(role="user", content=prompt)
            ]
        )

        sql = response.choices[0].message.content
        return sql.strip()