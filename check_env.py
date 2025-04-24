import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    print("Environment Variables:")
    print("NVIDIA_API_KEY:", "***" if os.getenv("NVIDIA_API_KEY") else "Not set")
    print("CONTENT_CREATOR_MODEL:", os.getenv("CONTENT_CREATOR_MODEL"))
    print("DIGITAL_ARTIST_MODEL:", os.getenv("DIGITAL_ARTIST_MODEL"))
    print("IMAGE_GENERATION_MODEL:", os.getenv("IMAGE_GENERATION_MODEL"))
    print("LOG_LEVEL:", os.getenv("LOG_LEVEL"))
    print("MAX_RETRIES:", os.getenv("MAX_RETRIES"))
    print("TIMEOUT:", os.getenv("TIMEOUT"))


if __name__ == "__main__":
    main()
