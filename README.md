# NVIDIA Agentic AI Solution

This project implements a human-in-the-loop AI agent system using NVIDIA's tech stack, following the architecture described in [NVIDIA's blog post](https://developer.nvidia.com/blog/build-your-first-human-in-the-loop-ai-agent-with-nvidia-nim/).

## Features

- Content Creator Agent: Generates promotional content for social media
- Digital Artist Agent: Creates visual content based on text descriptions
- Human-in-the-loop workflow: Allows human approval/rejection of generated content
- Modular architecture: Easy to extend and modify

## Prerequisites

- Python 3.8+
- NVIDIA API key
- Required Python packages (see requirements.txt)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your NVIDIA API key and model configurations

## Usage

1. Run the main workflow:
   ```bash
   python workflow.py
   ```
2. Enter a product description when prompted
3. Review the generated content and image
4. Provide feedback (yes/no) to approve or request new content

## Project Structure

```
.
├── agents/
│   ├── base_agent.py      # Base agent class
│   ├── content_creator.py # Content creation agent
│   └── digital_artist.py  # Image generation agent
├── workflow.py            # Main workflow orchestration
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Configuration

Edit the `.env` file to configure:
- NVIDIA API key
- Model selections
- API endpoints

## Contributing

Feel free to submit issues and enhancement requests!