from typing import Dict, Any, List
from pydantic import BaseModel, Field
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class ContentOutput(BaseModel):
    title: str = Field(description="Title of the promotion message")
    message: str = Field(description="The actual promotion message")
    tags: List[str] = Field(
        description="Hashtags for social media, usually starts with #"
    )


class ContentCreatorAgent(BaseAgent):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name, api_key)
        system_prompt = """You are an expert social media content creator.
        Your task is to create a different promotion message with the given product description.
        The output promotion message MUST use the following format:
        Title: a powerful, short message that depicts what this product is about
        Message: be creative for the promotion message, but make it short and ready for social media feeds
        Tags: the hashtags humans would normally use in social media
        
        Example format:
        Title: Stay Hydrated in Style
        Message: Keep your hydration game strong with our sleek 1L water bottle. Perfect for gym, office, or outdoor adventures!
        Tags: #StayHydrated #WaterBottle #Fitness #Lifestyle"""
        self._setup_chain(system_prompt)

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate that input contains a product description."""
        return "product_desc" in input_data and isinstance(
            input_data["product_desc"], str
        )

    def create_content(self, product_desc: str) -> ContentOutput:
        """Create promotional content for the given product description."""
        if not self.validate_input({"product_desc": product_desc}):
            raise ValueError(
                "Invalid input: product_desc is required and must be a string"
            )

        try:
            response = self.invoke({"input": product_desc})
            logger.debug(f"Raw response: {response}")

            # Parse the response into structured output
            lines = [line.strip() for line in response.split("\n") if line.strip()]

            # Find the relevant lines
            title_line = next(
                (line for line in lines if line.startswith("Title:")), None
            )
            message_line = next(
                (line for line in lines if line.startswith("Message:")), None
            )
            tags_line = next((line for line in lines if line.startswith("Tags:")), None)

            if not all([title_line, message_line, tags_line]):
                raise ValueError(
                    "Response format is incorrect. Missing required fields."
                )

            title = title_line.split("Title:")[1].strip()
            message = message_line.split("Message:")[1].strip()
            tags = [
                tag.strip() for tag in tags_line.split("Tags:")[1].strip().split(",")
            ]

            # Validate the output
            if not all([title, message, tags]):
                raise ValueError("Empty fields in the response")

            return ContentOutput(title=title, message=message, tags=tags)

        except Exception as e:
            logger.error(f"Error creating content: {str(e)}")
            logger.error(f"Response that caused error: {response}")
            raise
