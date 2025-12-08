import os
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionUserMessageParam


class TextToSqlCompletion:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint="https://sshya-mim76g3o-eastus2.cognitiveservices.azure.com/",
            api_key="8bG6sFkFBMVrdtpLBaFGMgvy1PJbHrhsQ6GHjTbKQRitNAKEhgk5JQQJ99BKACHYHv6XJ3w3AAAAACOG2iaY",
            api_version="2024-12-01-preview"
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