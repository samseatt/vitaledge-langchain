"""
File: config.py
Project: VitalEdge LangChain
Description: Centralized configuration management for VitalEdge LangChain. 
             Reads environment variables for service URLs, API keys, 
             and other global settings.

Author: Sam Seatt
Date: [Insert Date]

Features:
- Provides a `Config` class for accessing environment variables.
- Includes default values for configurations where applicable.

Explanation of Key Features:
- Centralized Configuration:
    The file acts as a central location for managing the connection details for all microservices.
    Uses Pydantic for validation and environment variable management.

- Environment Variable Integration:
    All configurations can be overridden using a .env file for flexibility across development, staging, and production.

- Future-Proof:
    Includes placeholders for an ML inference service, allowing seamless integration of new insights and enriching analysis in the future.
    Similarly, external LLMs (e.g., VitalEdge Open LLM) are integrated without breaking existing workflows.

- Timeouts:
    Configurable timeouts ensure that API calls to external services fail gracefully when they take too long.

- Extendable:
    Easy to add new services or modify existing settings without disrupting the current structure.

Usage:
    Import the `Config` class and use `Config.<VARIABLE_NAME>` to access 
    environment variables.

        from app.core.config import Config

        config = Config()

        # Example usage
        print(config.LLM_URL)  # Access the local LLM service URL
        print(config.TIMEOUT_SECONDS)  # Access the global timeout setting

Notes:
- Add required variables in the .env file for smooth operation.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Configuration settings for the VitalEdge LangChain project.

    Environment variables can be overridden using a `.env` file or system-wide settings.
    """

    # General settings
    PROJECT_NAME: str = Field(default="VitalEdge LangChain", description="The name of the project.")
    ENVIRONMENT: str = Field(default="development", description="Application environment: development, staging, production.")

    # VectorDB service settings
    VECTOR_DB_HOST: str = Field(default="127.0.0.1", description="Host for the VectorDB microservice.")
    VECTOR_DB_PORT: int = Field(default=8008, description="Port for the VectorDB microservice.")
    VECTOR_DB_URL: str = Field(default="http://127.0.0.1:8008", description="URL for the VectorDB microservice.")

    # Datalake service settings
    DATALAKE_HOST: str = Field(default="127.0.0.1", description="Host for the Datalake microservice.")
    DATALAKE_PORT: int = Field(default=8005, description="Port for the Datalake microservice.")
    DATALAKE_URL: str = Field(default="http://127.0.0.1:8005", description="URL for the Datalake microservice.")

    # Embeddings service settings
    EMBEDDINGS_HOST: str = Field(default="127.0.0.1", description="Host for the Embeddings microservice.")
    EMBEDDINGS_PORT: int = Field(default=8007, description="Port for the Embeddings microservice.")
    EMBEDDINGS_URL: str = Field(default="http://127.0.0.1:8007", description="URL for the Embeddings microservice.")

    # Local LLM service (VitalEdge LLM) settings
    LLM_HOST: str = Field(default="127.0.0.1", description="Host for the VitalEdge LLM microservice.")
    LLM_PORT: int = Field(default=8009, description="Port for the VitalEdge LLM microservice.")
    LLM_URL: str = Field(default="http://127.0.0.1:8009", description="URL for the VitalEdge LLM microservice.")

    # External LLM service (VitalEdge Open LLM) settings
    OPEN_LLM_HOST: str = Field(default="127.0.0.1", description="Host for the VitalEdge Open LLM microservice.")
    OPEN_LLM_PORT: int = Field(default=8010, description="Port for the VitalEdge Open LLM microservice.")
    OPEN_LLM_URL: str = Field(default="http://127.0.0.1:8010", description="URL for the VitalEdge Open LLM microservice.")

    # Placeholder for additional ML inference service (future integration)
    ML_INFERENCE_HOST: str = Field(default="127.0.0.1", description="Host for an optional ML inference microservice.")
    ML_INFERENCE_PORT: int = Field(default=8011, description="Port for the optional ML inference microservice.")
    ML_INFERENCE_URL: str = Field(default="http://127.0.0.1:8011", description="URL for the optional ML inference microservice.")

    # Global timeout settings for service calls
    TIMEOUT_SECONDS: int = Field(default=30, description="Timeout duration for HTTP requests to external services.")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Config()
