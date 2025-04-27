from typing import Dict, Any, Optional, TypedDict
from langgraph.graph import StateGraph, END
from agents.content_creator import ContentCreatorAgent, ContentOutput
from agents.digital_artist import DigitalArtistAgent
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import shutil

# Configure logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create AI_Response directory if it doesn't exist
AI_RESPONSE_DIR = "AI_Response"
os.makedirs(AI_RESPONSE_DIR, exist_ok=True)


class State(TypedDict):
    product_desc: str
    content: Optional[ContentOutput]
    image: Optional[Any]
    feedback: Optional[str]
    error: Optional[str]
    output_dir: Optional[str]  # New field for output directory


def create_output_directory() -> str:
    """Create a timestamped directory for storing outputs."""
    timestamp = datetime.now().strftime("%d%b%y_%H%M%S")
    output_dir = os.path.join(AI_RESPONSE_DIR, timestamp)
    os.makedirs(output_dir, exist_ok=True)

    # Set up file handler for logging
    log_file = os.path.join(output_dir, "execution.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    return output_dir


def create_agents() -> tuple[ContentCreatorAgent, DigitalArtistAgent]:
    """Create and initialize the agents."""
    try:
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")

        content_model = os.getenv(
            "CONTENT_CREATOR_MODEL", "meta/llama-3.1-405b-instruct"
        )
        artist_model = os.getenv(
            "DIGITAL_ARTIST_MODEL", "mistralai/mixtral-8x7b-instruct-v0.1"
        )
        image_model = os.getenv("IMAGE_GENERATION_MODEL", "stabilityai/sdxl-turbo")

        content_creator = ContentCreatorAgent(content_model, api_key)
        digital_artist = DigitalArtistAgent(artist_model, api_key, image_model)

        return content_creator, digital_artist
    except Exception as e:
        logger.error(f"Error creating agents: {str(e)}")
        raise


def create_content(state: State) -> State:
    """Create promotional content."""
    try:
        content_creator, _ = create_agents()
        state["content"] = content_creator.create_content(state["product_desc"])
        state["error"] = None
        logger.info(f"Content created successfully: {state['content']}")
    except Exception as e:
        logger.error(f"Error creating content: {str(e)}")
        state["error"] = str(e)
    return state


def generate_image(state: State) -> State:
    """Generate image based on content."""
    try:
        if state.get("error"):
            return state

        _, digital_artist = create_agents()
        state["image"] = digital_artist.generate_image(state["content"].title)
        state["error"] = None

        # Save the image to the output directory
        image_path = os.path.join(state["output_dir"], "output.jpg")
        state["image"].save(image_path)
        logger.info(f"Image saved to: {image_path}")
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        state["error"] = str(e)
    return state


def get_human_feedback(state: State) -> State:
    """Get human feedback on the generated content and image."""
    try:
        if state.get("error"):
            print(f"\nError occurred: {state['error']}")
            feedback = input("\nDo you want to try again? (yes/no): ")
            state["feedback"] = feedback.lower()
            return state

        print("\nGenerated Content:")
        print(f"Title: {state['content'].title}")
        print(f"Message: {state['content'].message}")
        print(f"Tags: {', '.join(state['content'].tags)}")

        if state.get("image"):
            image_path = os.path.join(state["output_dir"], "output.jpg")
            print(f"\nGenerated Image has been saved as '{image_path}'")

        feedback = input("\nDo you approve the content? (yes/no): ")
        state["feedback"] = feedback.lower()
        state["error"] = None
        logger.info(f"User feedback: {state['feedback']}")
    except Exception as e:
        logger.error(f"Error getting feedback: {str(e)}")
        state["error"] = str(e)
    return state


def should_continue(state: State) -> str:
    """Determine if we should continue based on human feedback."""
    if state.get("error"):
        return "create_content" if state["feedback"] == "yes" else "end"
    return "end" if state["feedback"] == "yes" else "create_content"


def main():
    try:
        # Create the workflow graph
        workflow = StateGraph(State)

        # Add nodes
        workflow.add_node("create_content", create_content)
        workflow.add_node("generate_image", generate_image)
        workflow.add_node("get_feedback", get_human_feedback)

        # Add edges
        workflow.add_edge("create_content", "generate_image")
        workflow.add_edge("generate_image", "get_feedback")
        workflow.add_conditional_edges(
            "get_feedback",
            should_continue,
            {"create_content": "create_content", "end": END},
        )

        # Set entry point
        workflow.set_entry_point("create_content")

        # Compile the workflow
        app = workflow.compile()

        # Run the workflow
        while True:
            product_desc = input(
                "Enter product description (or 'quit'/'exit' to exit): "
            )
            if product_desc.lower() in ["quit", "exit"]:
                logger.info("Program terminated by user")
                break

            # Create new output directory for this run
            output_dir = create_output_directory()
            logger.info(f"Starting new run in directory: {output_dir}")

            initial_state = State(
                product_desc=product_desc,
                content=None,
                image=None,
                feedback=None,
                error=None,
                output_dir=output_dir,
            )
            app.invoke(initial_state)

    except Exception as e:
        logger.error(f"Fatal error in main workflow: {str(e)}")
        raise


if __name__ == "__main__":
    main()
