from typing import Any, Dict, Optional
from pydantic import BaseModel
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

logger = logging.getLogger(__name__)


class BaseAgent:
    def __init__(self, model_name: str, api_key: str):
        """Initialize the base agent with model configuration."""
        try:
            if not api_key:
                raise ValueError("API key is required")
            if not model_name:
                raise ValueError("Model name is required")

            self.llm = ChatNVIDIA(model=model_name, nvidia_api_key=api_key)
            self.prompt_template = None
            self.chain = None
            logger.info(f"Initialized agent with model: {model_name}")
        except Exception as e:
            logger.error(f"Error initializing agent: {str(e)}")
            raise

    def _setup_chain(self, system_prompt: str):
        """Setup the agent's chain with the given system prompt."""
        try:
            if not system_prompt:
                raise ValueError("System prompt is required")

            self.prompt_template = ChatPromptTemplate.from_messages(
                [("system", system_prompt), ("user", "{input}")]
            )
            self.chain = self.prompt_template | self.llm | StrOutputParser()
            logger.info("Chain setup completed successfully")
        except Exception as e:
            logger.error(f"Error setting up chain: {str(e)}")
            raise

    def invoke(self, input_data: Dict[str, Any]) -> str:
        """Invoke the agent with the given input data."""
        try:
            if not self.chain:
                raise ValueError("Chain not initialized. Call _setup_chain first.")
            if not input_data:
                raise ValueError("Input data is required")

            result = self.chain.invoke(input_data)
            logger.info("Successfully invoked agent")
            return result
        except Exception as e:
            logger.error(f"Error invoking agent: {str(e)}")
            raise

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data. To be implemented by child classes."""
        try:
            if not isinstance(input_data, dict):
                raise ValueError("Input data must be a dictionary")
            return True
        except Exception as e:
            logger.error(f"Error validating input: {str(e)}")
            raise
