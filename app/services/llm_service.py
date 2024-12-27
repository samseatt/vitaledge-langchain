

import httpx
from app.core.config import config

class LLMService:
    """
    Handles text generation requests to the VitalEdge LLM microservice.
    """

    async def generate_text(self, prompt: str) -> str:
        print(f"LLMService.generate_text called with prompt: {prompt}")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.LLM_URL}/llm/generate",
                json={"prompt": prompt}
            )
            response.raise_for_status()
            print(f"LLMService.generate_text obtained response: {response.json().get('response', '')}")
            return response.json().get("response", "")
