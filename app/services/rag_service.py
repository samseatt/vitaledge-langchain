"""
File: app/services/rag_service.py

Implements Retrieval-Augmented Generation (RAG) using LangChain.
"""

# from langchain.chains import SimpleSequentialChain
# from langchain.prompts import PromptTemplate
# from langchain_community.llms import OpenAI
from app.core.langchain_tools import VectorDBSearchTool, EmbeddingsTool, LLMTool, DatalakeTool
from typing import List, Dict
# from app.core.config import Config
from app.core.config import config
import logging

# Logger for this file
logger = logging.getLogger(__name__)

class RAGService:
    """
    Handles the Retrieval-Augmented Generation (RAG) flow.
    """

    def __init__(self):
        self.embedding_tool = EmbeddingsTool(config.EMBEDDINGS_URL)
        self.vector_search_tool = VectorDBSearchTool(config.VECTOR_DB_URL)
        self.llm_tool = LLMTool(config.LLM_URL)
        self.datalake_tool = DatalakeTool(config.DATALAKE_URL)

    def process_query(self, query: str):
        """
        Executes the RAG pipeline for a given query.
        """
        # Step 0: Get relational data
        variants = self.datalake_tool._run(109)
        logger.info(f"*******Variants received: {variants}")
        context_data = "\n".join([
            f"- Variant: {item['variant']}, Genotype: {item['genotype']}, "
            f"Effect Size: {item['effect_size']}, Variant Frequency: {item['variant_frequency']}%, "
            f"Significance: {item['significance']}" for item in variants
        ])
        
        # Step 1: Generate Embeddings
        query_embedding = self.embedding_tool._run(query)
        # logger.debug(f"query_embedding returned query_embedding: {query_embedding}")

        # Step 2: Retrieve Relevant Context
        logger.info(f"Calling VectorDBSearchTool: {self.vector_search_tool.name}")
        context = self.vector_search_tool._run(query_embedding)
        logger.info(f"vector_search_tool.run returned context_results: {context}")

        # context = "\n".join([result["text"] for result in context_results])

        # Step 3: Construct a prompt for the LLM
        # combined_prompt = self._construct_prompt(query, context)
        # print(f"Called RAGOrchestrator._construct_prom and recieved combined prompt: {combined_prompt}")

        # Step 4: Generate Final Answer
        response = self.llm_tool._run(query, context, context_data)

        return {
            "query": query,
            "response": response,
            "context": context
        }

        # return response

    # def _construct_prompt(self, query: str, context: List[Dict]) -> str:
    #     """
    #     Combines the query and retrieved context into a single prompt.
    #     """
    #     print(f"Calling RAGOrchestrator._construct_prompt with query: {query} and context: {context}")
    #     context_text = "\n".join([item["text"] for item in context if "text" in item])
    #     print(f"Join generated context_text: {context_text}")
    #     prompt = f"Context:\n{context_text}\n\nQuery:\n{query}"
    #     print(f"Constructed prompt: {prompt}")
    #     return prompt
