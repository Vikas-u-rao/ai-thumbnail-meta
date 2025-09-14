#!/usr/bin/env python3
"""
AI Thumbnail & Metadata Generator
Main entry point for the application
"""

import os
from config import current_hf_token, current_openrouter_token
from ui import create_gradio_ui

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Using system environment variables only.")

def main():
    """Main function to launch the application"""
    print("🚀 Starting AI Thumbnail & Metadata Generator...")
    print("💡 Using OpenRouter API for text generation and Hugging Face for images")
    print("⚠️  Note: Set API keys in the app UI for authenticated access")
    
    # Check if tokens are available from environment
    hf_env_token = os.getenv('HF_TOKEN')
    openrouter_env_token = os.getenv('OPENROUTER_TOKEN')
    
    if hf_env_token:
        print("✅ Hugging Face token detected from environment")
        # Set global token if found in environment
        import config
        config.current_hf_token = hf_env_token
        
    if openrouter_env_token:
        print("✅ OpenRouter token detected from environment")
        # Set global token if found in environment
        import config
        config.current_openrouter_token = openrouter_env_token
    
    if not hf_env_token and not openrouter_env_token:
        print("⚠️  No API tokens found in environment - use the app UI to set them")
    
    # Create and launch the Gradio app
    app = create_gradio_ui()
    
    app.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )

if __name__ == "__main__":
    main()