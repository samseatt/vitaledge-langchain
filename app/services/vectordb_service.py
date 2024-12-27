"""
File: vector_retrieval.py
Project: VitalEdge LangChain
Description: Handles document retrieval from VectorDB using FAISS or Weaviate. 
             Supports searching for contextually relevant embeddings.

Author: Sam Seatt
Date: [Insert Date]

Features:
- Searches VectorDB for top-k relevant embeddings based on input queries.
- Handles VectorDB interactions through RESTful APIs.

Usage:
    Import this module and call `search_vectordb(query: str, top_k: int)` 
    to retrieve relevant documents.

Notes:
- Ensure VectorDB is populated with embeddings before using this module.
"""

import httpx
from app.core.config import config

class VectorDBService:
    """
    Handles vector search requests to the VitalEdge VectorDB microservice.
    """

    async def search_vectors(self, query_vector: list, top_k: int = 5) -> list:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.VECTOR_DB_URL}/search/search",
                json={"query_vector": query_vector, "top_k": top_k}
            )
            print(f"VectorDBService.search_vectors returned response: {response.json()}")
            response.raise_for_status()
            return response.json().get("results", [])
