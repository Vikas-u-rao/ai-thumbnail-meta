import io
from PIL import Image, ImageDraw, ImageFont
from config import IMAGE_MODELS, HF_IMAGE_API_URL, STYLE_PROMPTS
from api_utils import query_hf_api


def create_placeholder_image(prompt):
    """Create a placeholder image when generation fails"""
    try:
        img = Image.new('RGB', (1280, 720), color=(100, 149, 237))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Add title
        title = "Placeholder Thumbnail"
        if font:
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1280 - text_width) // 2
            draw.text((x, 200), title, fill='white', font=font)
        
        # Add prompt
        prompt_text = f"Topic: {prompt[:50]}..."
        if font:
            bbox = draw.textbbox((0, 0), prompt_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1280 - text_width) // 2
            draw.text((x, 300), prompt_text, fill='lightgray', font=font)
        
        # Add note
        note = "AI generation failed - using placeholder"
        if font:
            bbox = draw.textbbox((0, 0), note, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1280 - text_width) // 2
            draw.text((x, 400), note, fill='yellow', font=font)
        
        return img
    except Exception as e:
        print(f"Error creating placeholder: {e}")
        # Ultimate fallback - solid color
        return Image.new('RGB', (1280, 720), color=(100, 149, 237))


def add_text_overlay(image, title_text, style="bold"):
    """Add text overlay to image"""
    if image is None:
        return None
    
    # Create a copy to avoid modifying original
    img = image.copy()
    draw = ImageDraw.Draw(img)
    
    # Get image dimensions
    width, height = img.size
    
    # Try to load fonts
    try:
        if style == "bold":
            font_size = max(24, width // 20)
            font = ImageFont.truetype("arial.ttf", font_size)
        elif style == "elegant":
            font_size = max(20, width // 25)
            font = ImageFont.truetype("times.ttf", font_size)
        else:  # clean
            font_size = max(18, width // 30)
            font = ImageFont.truetype("calibri.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Wrap text to fit image width
    words = title_text.split()
    lines = []
    current_line = ""
    max_width = width * 0.8
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] < max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # Position text (top third of image)
    y_start = height // 6
    line_height = font_size + 5
    
    for i, line in enumerate(lines[:3]):  # Max 3 lines
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = y_start + (i * line_height)
        
        # Draw shadow/outline for better visibility
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            draw.text((x + dx, y + dy), line, fill='black', font=font)
        
        # Draw main text
        draw.text((x, y), line, fill='white', font=font)
    
    return img


def generate_image(prompt, model_choice="fast"):
    """Generate image using Hugging Face Inference API"""
    try:
        model_name = IMAGE_MODELS[model_choice]
        api_url = HF_IMAGE_API_URL + model_name
        
        payload = {"inputs": prompt}
        
        print(f"Attempting to generate image with {model_choice}...")
        response = query_hf_api(api_url, payload)
        
        if response and response.status_code == 200:
            try:
                image = Image.open(io.BytesIO(response.content))
                print(f"✅ Image generated successfully with {model_choice}")
                return image
            except Exception as img_error:
                print(f"❌ Error opening image: {img_error}")
                return create_placeholder_image(prompt)
        else:
            print(f"❌ Image generation failed for {model_choice}")
            return create_placeholder_image(prompt)
            
    except Exception as e:
        print(f"❌ Error generating image with {model_choice}: {e}")
        return create_placeholder_image(prompt)


def generate_thumbnails(topic, style, text_overlay="", overlay_style="bold"):
    """Generate two thumbnails with different models"""
    print(f"Generating thumbnails for: {topic} in {style} style")
    
    # Get style prompt
    style_prompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["Realistic"])
    
    # Create enhanced prompts
    base_prompt = f"YouTube thumbnail, {topic}, {style_prompt}, eye-catching, professional, high contrast, vibrant colors, no text"
    
    # Generate with both models
    prompt1 = f"{base_prompt}, centered composition"
    prompt2 = f"{base_prompt}, dynamic angle, creative layout"
    
    print("Generating thumbnail 1 (Fast)...")
    thumbnail1 = generate_image(prompt1, "fast")
    
    print("Generating thumbnail 2 (Quality)...")
    thumbnail2 = generate_image(prompt2, "quality")
    
    # Resize to YouTube thumbnail dimensions (16:9)
    target_size = (1280, 720)
    if thumbnail1:
        thumbnail1 = thumbnail1.resize(target_size, Image.Resampling.LANCZOS)
    if thumbnail2:
        thumbnail2 = thumbnail2.resize(target_size, Image.Resampling.LANCZOS)
    
    # Add text overlay if provided
    if text_overlay.strip():
        if thumbnail1:
            thumbnail1 = add_text_overlay(thumbnail1, text_overlay, overlay_style)
        if thumbnail2:
            thumbnail2 = add_text_overlay(thumbnail2, text_overlay, overlay_style)
    
    return thumbnail1, thumbnail2