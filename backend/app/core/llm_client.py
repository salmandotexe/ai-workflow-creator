import openai
from constants import SYSTEM_PROMPT_WORKFLOW_GENERATOR
from config import settings
from abc import ABC

class LLMClient(ABC):
    def __init__(self, system_prompt: str = None, client=None):
        self.system_prompt = system_prompt
        self.client = client
    
    def generate_workflow(self, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses.")
    

class OpenAIClient(LLMClient):
    def __init__(self, system_prompt: str = None, client: openai= None):
        super().__init__(system_prompt, client)

        if not self.system_prompt or self.client is None:
            raise ValueError("System prompt and OpenAI client must be initialized.")
        self.client = client or openai
        self.client.api_key = settings.OPENAI_API_KEY

    def generate_workflow(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

def get_llm_client(system_prompt: str = None, client: openai = None) -> OpenAIClient:
    return OpenAIClient(system_prompt=SYSTEM_PROMPT_WORKFLOW_GENERATOR, client=openai)