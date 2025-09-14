# Configuration file for AI Thumbnail & Metadata Generator

# API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
HF_IMAGE_API_URL = "https://api-inference.huggingface.co/models/"

# Model configurations
TEXT_MODELS = {
    "deepseek-r1-free": "deepseek/deepseek-r1:free"  # Use deepseek model for OpenRouter
}

IMAGE_MODELS = {
    "fast": "black-forest-labs/FLUX.1-schnell",  # Fast FLUX model  
    "quality": "black-forest-labs/FLUX.1-dev"   # Quality FLUX model
}

# Style prompts for different thumbnail styles
STYLE_PROMPTS = {
    "Realistic": "photorealistic, high quality, professional photography, detailed, sharp focus",
    "Cartoon": "cartoon style, animated, colorful, fun, illustrated, digital art, vibrant",
    "Cinematic": "cinematic lighting, dramatic, movie poster style, epic, atmospheric, high contrast",
    "Minimalist": "minimalist design, clean, simple, modern, elegant, white background, typography",
    "Gaming": "gaming style, neon colors, futuristic, glowing effects, action-packed",
    "Tech": "tech style, sleek, modern, blue and white, professional, corporate"
}

# Global variables for API keys
current_hf_token = ""
current_openrouter_token = ""