from openai import OpenAI
from app.constants import SYSTEM_PROMPT_WORKFLOW_GENERATOR
from app.core.config import settings
from abc import ABC, abstractmethod

class LLMClient(ABC):
    """Abstract base class for a Large Language Model client."""
    def __init__(self, system_prompt: str, client):
        self.system_prompt = system_prompt
        self.client = client
    
    @abstractmethod
    def generate_workflow(self, prompt: str) -> str:
        """Generates a workflow based on a given prompt."""
        raise NotImplementedError("This method should be overridden by subclasses.")

class OpenAIClient(LLMClient):
    """A client for interacting with the OpenAI API."""
    
    # 1. Use the correct type hint 'OpenAI' instead of the module 'openai'.
    def __init__(self, system_prompt: str, client: OpenAI = None):
        
        # 2. Modernize client instantiation for openai v1.0+.
        #    Create a new client if one isn't provided.
        if client is None:
            if not settings.OPENAI_API_KEY:
                raise ValueError("The OPENAI_API_KEY must be set in your settings.")
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # 3. Call the parent constructor.
        super().__init__(system_prompt=system_prompt, client=client)

    def generate_workflow(self, prompt: str) -> str:
        """
        Generates a workflow by calling the OpenAI Chat Completions API.
        
        Note: The parameter name was changed from 'message' to 'prompt'
        to match the base class for consistency.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

def get_llm_client() -> OpenAIClient:
    """
    Factory function to get a pre-configured OpenAIClient instance.
    The function is simplified to remove redundant parameters.
    """
    return OpenAIClient(system_prompt=SYSTEM_PROMPT_WORKFLOW_GENERATOR)