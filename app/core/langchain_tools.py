"""
File: app/core/langchain_tools.py

Defines custom LangChain tools to interact with VitalEdge microservices.
"""

from langchain.tools import BaseTool
from pydantic import PrivateAttr
import requests
from typing import List, Dict
import logging

# Logger for this file
logger = logging.getLogger(__name__)

class DatalakeTool(BaseTool):
    """
    Tool to retrieve relational data from datalake using VitalEdge Datalake microservice.
    """
    # name = "datalake_query"
    # description = "Search the Datalake database for relational data."
    name: str = "datalake_query"
    description: str = "%%%%%%%%%%%%%Search the Datalake database for relational data."
    _base_url: str = PrivateAttr()  # Define as a private attribute

    def __init__(self, base_url: str, **kwargs):
        super().__init__(**kwargs)
        self._base_url = base_url

    # async def search_vectors(self, query_vector: list, top_k: int = 5) -> list:

    def _run(self, study_id: int):
        logging.debug(f"DatalakeTool.run called with study_id: {study_id}")
        # payload = {"study_id": study_id}
        logging.debug(f"DatalakeTool.run posting to endpoint: {self._base_url}")
        response = requests.get(f"{self._base_url}/studies/variants_by_study/{study_id}")
        logging.debug(f"DatalakeTool.run received a response: {response.json()}")
        return response.json()

class VectorDBSearchTool(BaseTool):
    """
    Tool to perform vector similarity search using VitalEdge VectorDB microservice.
    """
    # name = "vector_search"
    # description = "Search the vector database for contextually relevant embeddings."
    name: str = "vector_search"
    description: str = "Search the vector database for contextually relevant embeddings."
    _base_url: str = PrivateAttr()  # Define as a private attribute

    def __init__(self, base_url: str, **kwargs):
        super().__init__(**kwargs)
        self._base_url = base_url

    # async def search_vectors(self, query_vector: list, top_k: int = 5) -> list:

    def _run(self, query_embedding: list, top_k: int = 1):
        logging.debug(f"VectorDBSearchTool.run called with top_k: {top_k}")
        payload = {"query_vector": query_embedding, "top_k": top_k}
        logging.debug(f"VectorDBSearchTool.run posting to endpoint: {self._base_url}")
        response = requests.post(f"{self._base_url}/search/search", json=payload)
        logging.debug(f"VectorDBSearchTool.run received a response: {response.json()}")
        return response.json()["results"]


class EmbeddingsTool(BaseTool):
    """
    Tool to generate embeddings using VitalEdge Embeddings microservice.
    """
    # name = "generate_embeddings"
    # description = "Generate embeddings for a given text."
    name: str = "generate_embeddings"
    description: str = "Generate embeddings for a given text."
    _base_url: str = PrivateAttr()  # Define as a private attribute

    def __init__(self, base_url: str, **kwargs):
        super().__init__(**kwargs)
        self._base_url = base_url
        

    def _run(self, text: str):
        payload = {"texts": [text]}
        response = requests.post(f"{self._base_url}/embeddings/generate", json=payload)
        return response.json()["embeddings"][0]
        # embeddings = response.json().get("embeddings")
        # return embeddings[0]  # Return the first embedding


class LLMTool(BaseTool):
    """
    Tool to generate responses using VitalEdge LLM microservice.
    """
    name: str = "generate_text"
    description:str = "Generate a text response based on the query and context."
    _base_url: str = PrivateAttr()  # Define as a private attribute

    def __init__(self, base_url: str, **kwargs):
        super().__init__(**kwargs)
        self._base_url = base_url

    def _run(self, query: str, context: str, context_data: str):
        combined_prompt = self._construct_prompt(query, context, context_data)
        payload = {"prompt": combined_prompt}

        # payload = {"text": query, "context": context}
        logger.info(f"Calling LLM with payload ...\n")
        logger.info(payload)
        response = requests.post(f"{self._base_url}/llm/generate", json=payload)
        # response = "test"
        return response.json()["response"]

    def _construct_prompt(self, query: str, context: List[Dict], context_data: str) -> str:
        """
        Combines the query and retrieved context into a single prompt.
        """
        print(f"Calling RAGOrchestrator._construct_prompt with query: {query} and context: {context}")
        # context_text = "\n".join([item["text"] for item in context if "text" in item])
        context_text = "\n".join([item["metadata"]["text"] for item in context if "metadata" in item and "text" in item["metadata"]])
        print(f"Join generated context_text: {context_text}")
        full_context = f"{context_text}\n\n{context_data}"
        prompt = f"Context:\n{full_context}\n\nQuery:\n{query}"
        print(f"$$$$$$$$$$$$$Constructed prompt: {prompt}")
        return prompt
