"""
File: embeddings_service.py
Project: VitalEdge LangChain
Description: Service module for interfacing with the VitalEdge Embeddings microservice. 
             This module provides functionality to generate text embeddings required 
             for retrieval and other downstream tasks.

Author: Sam Seatt
Date: [Insert Date]

Features:
- Sends text data to the VitalEdge Embeddings microservice for embedding generation.
- Processes and validates embedding responses.
- Supports both single-text and batch embedding generation.

Usage:
    Import the `EmbeddingsService` class and call its methods to interact with 
    the embeddings microservice.

Example:
    from app.services.embeddings_service import EmbeddingsService

    embeddings_service = EmbeddingsService()
    embeddings = embeddings_service.generate_embeddings(["Sample text for embedding."])
    print(embeddings)

Notes:
- Ensure the VitalEdge Embeddings microservice is running and its endpoint is 
  correctly configured in the `.env` file.
- The service depends on HTTP requests using the `httpx` library. Handle network 
  errors appropriately when integrating with this service.

Dependencies:
- `httpx`: Used for HTTP communication with the embeddings microservice.

"""

import httpx
from app.core.config import config

class EmbeddingsService:
    """
    Handles embedding requests to the VitalEdge Embeddings microservice.
    """

    async def generate_embedding(self, text: str) -> list:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.EMBEDDINGS_URL}/embeddings/generate",
                json={"texts": [text]}
            )
            response.raise_for_status()
            embeddings = response.json().get("embeddings")
            return embeddings[0]  # Return the first embedding
