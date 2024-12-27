"""
File: rag.py
Project: VitalEdge LangChain
Description: Contains the core RAG (Retrieval-Augmented Generation) flow 
             for VitalEdge LangChain. Coordinates between VectorDB, Embeddings,
             and LLM microservices to generate insights.

Author: Sam Seatt
Date: [Insert Date]

Features:
- Retrieves contextually relevant documents from VectorDB.
- Generates embeddings using the VitalEdge Embeddings microservice.
- Interacts with LLM (local or external) for generating responses.

Usage:
    Import this module and call `rag_workflow(prompt: str)` for RAG-based 
    text generation.

Notes:
- This module depends on configured access to VectorDB, Embeddings, and LLM 
  microservices. Ensure the service URLs are valid in the .env file.
"""

from fastapi import APIRouter, HTTPException
from app.services.rag_service import RAGService
from app.core.rag_orchestrator import RAGOrchestrator
from pydantic import BaseModel
# from typing import Dict
import logging

# Logger for this file
logger = logging.getLogger(__name__)

router = APIRouter()
rag_orchestrator = RAGOrchestrator()
rag_service = RAGService()

class RAGRequest(BaseModel):
    query: str

class RAGResponse(BaseModel):
    query: str
    response: str
    context: list


# @router.post("/rag")
# async def rag(query: str):
#     """
#     Endpoint to handle RAG-based query processing.
#     """
#     response = rag_service.process_query(query)
#     return {"response": response}

@router.post("/rag", response_model=RAGResponse)
async def rag(request: RAGRequest):
    """
    Endpoint to handle RAG-based query processing.
    """
    logger.info(f"rag endpoint called with query: {request.query}")
    try:
        result = rag_service.process_query(request.query)
        logger.info(f"rag route received the following result form rag_orchestrator.run: {result}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in RAG workflow: {str(e)}")


@router.post("/rag_no_langchain", response_model=RAGResponse)
async def orchestrate_rag(request: RAGRequest):
    """
    Endpoint for RAG workflow orchestration.
    """
    try:
        result = await rag_orchestrator.run(request.query)
        logger.info(f"$$$$$$$$$$$$$$$$ orchestrate_rag route received the following result form rag_orchestrator.run: {result}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in RAG workflow: {str(e)}")
