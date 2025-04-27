# NVIDIA Agentic AI Solution

This project implements a human-in-the-loop AI agent system using NVIDIA's tech stack, following the architecture described in [NVIDIA's blog post](https://developer.nvidia.com/blog/build-your-first-human-in-the-loop-ai-agent-with-nvidia-nim/).

## Features

- Content Creator Agent: Generates promotional content for social media
- Digital Artist Agent: Creates visual content based on text descriptions
- Human-in-the-loop workflow: Allows human approval/rejection of generated content
- Modular architecture: Easy to extend and modify

## Technical Stack

| Component | Technology/Tool |
|-----------|----------------|
| Models | - Content Creation: meta/llama-3.1-405b-instruct<br>- Digital Artist: mistralai/mixtral-8x7b-instruct-v0.1<br>- Image Generation: stabilityai/stable-diffusion-3-medium |
| Framework | - LangChain<br>- LangGraph<br>- NVIDIA NIM Microservice Endpoints |
| Core Dependencies | - PyTorch 2.2.2<br>- Python 3.10+ |
| Vector Database | Milvus (configured through NVIDIA AI Endpoints) |
| Supported File Types | Images (output as JPG) |

## Prerequisites

- Python 3.8+
- NVIDIA API key
- Required Python packages (see requirements.txt)
- Docker and Docker Compose (for containerized deployment)
- NVIDIA Container Toolkit (for GPU support)

## Setup

### Local Development Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your NVIDIA API key and model configurations

### Docker Deployment
1. Ensure you have Docker and NVIDIA Container Toolkit installed
2. Build and run the container:
   ```bash
   docker-compose up --build
   ```
3. The application will be available at `http://localhost:7860`

### AWS EC2 Deployment
1. Launch an EC2 instance with:
   - Ubuntu 22.04 LTS
   - GPU instance type (e.g., g4dn.xlarge or larger)
   - NVIDIA GPU drivers pre-installed
2. Install Docker and NVIDIA Container Toolkit:
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install NVIDIA Container Toolkit
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
      && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   
   sudo apt-get update
   sudo apt-get install -y nvidia-docker2
   sudo systemctl restart docker
   ```
3. Clone the repository and deploy:
   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   docker-compose up -d
   ```
4. Access the application at `http://<ec2-public-ip>:7860`

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
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # This file
```

## Configuration

Edit the `.env` file to configure:
- NVIDIA API key
- Model selections
- API endpoints

## Contributing

Feel free to submit issues and enhancement requests!