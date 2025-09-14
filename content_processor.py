import json
from datetime import datetime


def create_download_data(topic, metadata, thumbnail1, thumbnail2, selected_thumbnail):
    """Create downloadable JSON data"""
    # Parse metadata
    lines = metadata.split('\n')
    title = ""
    description = ""
    tags = ""
    
    for line in lines:
        if line.startswith('TITLE:'):
            title = line.replace('TITLE:', '').strip()
        elif line.startswith('DESCRIPTION:'):
            description = line.replace('DESCRIPTION:', '').strip()
        elif line.startswith('TAGS:'):
            tags = line.replace('TAGS:', '').strip()
    
    data = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "metadata": {
            "title": title,
            "description": description,
            "tags": tags.split(', ') if tags else []
        },
        "selected_thumbnail": selected_thumbnail,
        "thumbnails_generated": 2
    }
    
    return json.dumps(data, indent=2)


def process_content(topic, style, model_choice, text_overlay, overlay_style):
    """Main function to generate all content"""
    if not topic.strip():
        return "Please enter a topic!", None, None, ""
    
    print(f"Processing: {topic}")
    
    # Generate metadata
    print("Generating metadata...")
    from metadata_generator import generate_metadata
    metadata = generate_metadata(topic, model_choice)
    
    print("Generating thumbnails...")
    from image_generator import generate_thumbnails
    thumbnail1, thumbnail2 = generate_thumbnails(topic, style, text_overlay, overlay_style)
    
    print("Complete!")
    
    # Create download data
    download_data = create_download_data(topic, metadata, thumbnail1, thumbnail2, "thumbnail1")
    
    return metadata, thumbnail1, thumbnail2, download_data