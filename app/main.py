"""
File: main.py
Project: VitalEdge LangChain
Description: Entry point for the FastAPI application that orchestrates 
             LangChain-based RAG (Retrieval-Augmented Generation) workflows.

Author: Sam Seatt
Date: [Insert Date]

Features:
- Initializes the FastAPI application with endpoints for RAG workflows.
- Registers routers for seamless interaction with external services (VectorDB, LLM, etc.).
- Centralized middleware and event handlers for managing application lifecycle.

Usage:
    Start the application with:
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Notes:
- Ensure that the .env file is configured with correct API keys and service URLs.
"""

from fastapi import FastAPI
from app.api.routes.rag import router as rag_router
from app.utils.logging import setup_logging

# Set up logging for the application
setup_logging(log_level="DEBUG", log_file="logs/vitaledge_langchain.log")

app = FastAPI()

# Include the RAG route
app.include_router(rag_router, prefix="/orchestrate", tags=["RAG"])


@app.get("/")
async def root():
    return {"message": "Welcome to VitalEdge LangChain!"}
