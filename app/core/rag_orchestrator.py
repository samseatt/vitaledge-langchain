"""
File: rag_orchestrator.py
Project: VitalEdge LangChain
Description: Core orchestrator module for the Retrieval-Augmented Generation (RAG) 
             workflow in VitalEdge LangChain. This module coordinates interactions 
             between the VectorDB, Embeddings, and LLM microservices to enable 
             contextually-aware response generation.

             NOTE: This module does not use a LangChain but uses a simpler, direct
             approach that is less extensible than the LangChain based flows.

Author: Sam Seatt
Date: December 7, 2024

Features:
- Executes RAG workflows by integrating multiple microservices.
- Retrieves top-k relevant documents from VectorDB.
- Generates query embeddings using VitalEdge Embeddings microservice.
- Passes context and queries to the LLM microservice for final response generation.

Usage:
    Import the `RAGOrchestrator` class and call `run_rag_workflow(prompt: str)` 
    to execute a complete RAG workflow.

Example:
    from app.core.rag_orchestrator import RAGOrchestrator

    orchestrator = RAGOrchestrator()
    response = orchestrator.run_rag_workflow("What are the symptoms of diabetes?")
    print(response)

Notes:
- The RAGOrchestrator class acts as the central point for workflow management.
- Ensure that all microservices (VectorDB, Embeddings, and LLM) are up and running 
  and their endpoints are correctly configured in the `.env` file.
"""

from app.services.datalake_service import DatalakeService
from app.services.embeddings_service import EmbeddingsService
from app.services.vectordb_service import VectorDBService
from app.services.llm_service import LLMService
from typing import Dict, List

class RAGOrchestrator:
    """
    Orchestrates the Retrieval-Augmented Generation (RAG) flow.
    """

    def __init__(self):
        self.datalake_service = DatalakeService
        self.embeddings_service = EmbeddingsService()
        self.vectordb_service = VectorDBService()
        self.llm_service = LLMService()

    async def run(self, query: str) -> Dict:
        """
        Executes the RAG workflow.
        """
        print(f"RAGOrchestrator.run called with query: {query}")

        # Step 0: Get data from Datalake
        print(f"@@@@@@@@@@@@@@@@@ Reading variants")
        variants = await self.datalake_service.search_variants(103)
        print(f"@@@@@@@@@@@@@@@@@Variants read: {variants}")

        # Step 1: Generate query embeddings
        embeddings = await self.embeddings_service.generate_embedding(query)

        # Step 2: Search for relevant context
        print(f"Calling vectordb_service.search_vectors with embeddings: {embeddings}")
        context = await self.vectordb_service.search_vectors(embeddings)
        print(f"Called vectordb_service.search_vectors with context {context}")

        # Step 3: Construct a prompt for the LLM
        combined_prompt = self._construct_prompt(query, context)
        print(f"Called RAGOrchestrator._construct_prom and recieved combined prompt: {combined_prompt}")

        # Step 4: Generate a response using the LLM
        response = await self.llm_service.generate_text(combined_prompt)

        print(f"$$$$$$$$$$$$ RAGOrchestrator.run Returning response: {response}")

        return {
            "query": query,
            "response": response,
            "context": context
        }


    def _construct_prompt(self, query: str, context: List[Dict]) -> str:
        """
        Combines the query and retrieved context into a single prompt.
        """
        print(f"Calling RAGOrchestrator._construct_prompt with query: {query} and context: {context}")
        context_text = "\n".join([item["text"] for item in context if "text" in item])
        print(f"Join generated context_text: {context_text}")
        prompt = f"Context:\n{context_text}\n\nQuery:\n{query}"
        print(f"Constructed prompt: {prompt}")
        return prompt

