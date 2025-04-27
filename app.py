import gradio as gr
from workflow import (
    State,
    create_agents,
    create_content,
    generate_image,
    create_output_directory,
)
import os
from dotenv import load_dotenv
import logging
from PIL import Image
import io
import numpy as np

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_product_description(
    product_desc: str,
) -> tuple[str, str, str, str, np.ndarray]:
    """Process the product description and generate content and image."""
    try:
        # Create output directory
        output_dir = create_output_directory()

        # Initialize state
        state = State(
            product_desc=product_desc,
            content=None,
            image=None,
            feedback=None,
            error=None,
            output_dir=output_dir,
        )

        # Generate content
        state = create_content(state)
        if state.get("error"):
            return state["error"], "", "", "", None

        # Generate image
        state = generate_image(state)
        if state.get("error"):
            return state["error"], "", "", "", None

        # Convert PIL Image to numpy array for Gradio
        img_array = np.array(state["image"])

        return (
            "",  # No error
            state["content"].title,
            state["content"].message,
            ", ".join(state["content"].tags),
            img_array,
        )

    except Exception as e:
        logger.error(f"Error in process_product_description: {str(e)}")
        return str(e), "", "", "", None


# Create Gradio interface
with gr.Blocks(
    title="NVIDIA Agentic AI Content Generator", theme=gr.themes.Soft()
) as demo:
    gr.Markdown("# NVIDIA Agentic AI Content Generator")
    gr.Markdown(
        "Enter a product description to generate promotional content and images."
    )

    with gr.Row():
        with gr.Column():
            product_input = gr.Textbox(
                label="Product Description",
                placeholder="Enter a detailed description of your product...",
                lines=3,
            )
            submit_btn = gr.Button("Generate Content", variant="primary")

    with gr.Row():
        with gr.Column():
            error_output = gr.Textbox(label="Error", visible=False)
            title_output = gr.Textbox(label="Generated Title")
            message_output = gr.Textbox(label="Generated Message", lines=3)
            tags_output = gr.Textbox(label="Generated Tags")
            image_output = gr.Image(label="Generated Image", type="numpy")

    # Set up the processing function
    submit_btn.click(
        fn=process_product_description,
        inputs=[product_input],
        outputs=[error_output, title_output, message_output, tags_output, image_output],
    )

if __name__ == "__main__":
    demo.launch(share=True)
