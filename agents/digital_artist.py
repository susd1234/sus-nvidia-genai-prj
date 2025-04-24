import requests
import base64
from io import BytesIO
from PIL import Image
from typing import Dict, Any
from .base_agent import BaseAgent
import logging
import time
import json

logger = logging.getLogger(__name__)


class DigitalArtistAgent(BaseAgent):
    def __init__(self, model_name: str, api_key: str, image_model: str):
        super().__init__(model_name, api_key)
        self.image_model = image_model
        self.api_key = api_key
        system_prompt = """You are an expert digital artist.
        Your task is to transform text descriptions into creative visual prompts.
        Focus on creating vivid, detailed descriptions that would make great images.
        The prompt should be detailed but concise, focusing on key visual elements.
        Example: For a water bottle, describe its shape, material, color, and any unique features."""
        self._setup_chain(system_prompt)

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate that input contains a text description."""
        return "text" in input_data and isinstance(input_data["text"], str)

    def generate_image(self, text: str, max_retries: int = 3) -> Image.Image:
        """Generate an image from the given text description."""
        if not self.validate_input({"text": text}):
            raise ValueError("Invalid input: text is required and must be a string")

        try:
            # First, enhance the text description
            enhanced_prompt = self.invoke({"input": text})
            logger.debug(f"Enhanced prompt: {enhanced_prompt}")

            # Generate image using NVIDIA's API
            invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            }

            payload = {
                "prompt": enhanced_prompt,
                "cfg_scale": 7.5,
                "aspect_ratio": "1:1",
                "seed": 0,
                "steps": 50,
                "negative_prompt": "blurry, low quality, distorted, deformed",
            }

            logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")

            for attempt in range(max_retries):
                try:
                    response = requests.post(
                        invoke_url,
                        headers=headers,
                        json=payload,
                        timeout=120,  # Increased timeout to 120 seconds
                    )
                    response.raise_for_status()

                    # Parse the response
                    response_data = response.json()
                    logger.debug(
                        f"Response data: {json.dumps(response_data, indent=2)}"
                    )

                    # Handle the response format
                    if isinstance(response_data, dict):
                        # Check if the API wraps the B64 in an "image" field
                        image_b64 = response_data.get("image")
                        if isinstance(image_b64, str):
                            image_data = base64.b64decode(image_b64)
                        else:
                            logger.error(
                                f"Missing or invalid image data in response: {response_data}"
                            )
                            raise ValueError("Response missing image data")
                    else:
                        logger.error(f"Unexpected response type: {type(response_data)}")
                        raise ValueError("Unexpected response type")

                    return Image.open(BytesIO(image_data))

                except requests.exceptions.RequestException as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(2**attempt)  # Exponential backoff
                    else:
                        raise

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise
