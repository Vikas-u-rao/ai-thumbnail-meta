# AI Thumbnail & Metadata Generator

A modular Python application that generates YouTube thumbnails and metadata using AI models.

## File Structure

```
thumbnail_generator/
├── main.py                 # Main entry point
├── config.py              # Configuration and constants
├── ui.py                  # Gradio user interface
├── api_utils.py           # API utilities and token testing
├── metadata_generator.py  # Text/metadata generation
├── image_generator.py     # Image/thumbnail generation
├── content_processor.py   # Main content processing logic
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Features

- 🤖 AI-powered metadata generation using OpenRouter API
- 🎨 Dual thumbnail generation using Hugging Face FLUX models
- 🎯 6 different visual styles (Realistic, Cartoon, Cinematic, etc.)
- ✏️ Custom text overlay editor
- 📥 JSON export for metadata
- 🔑 Separate API key management for each service

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Open your browser to `http://localhost:7860`

4. Set your API keys in the UI:
   - OpenRouter API key for text generation
   - Hugging Face API key for image generation

## API Keys

- **OpenRouter**: Get your key at [https://openrouter.ai/](https://openrouter.ai/)
- **Hugging Face**: Get your key at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## Usage

1. Enter your video topic
2. Choose thumbnail style and text model
3. Add custom text overlay (optional)
4. Generate content and download!

## Modules

- **config.py**: Contains all configuration constants and global variables
- **api_utils.py**: Handles API interactions and token validation
- **metadata_generator.py**: Generates YouTube titles, descriptions, and tags
- **image_generator.py**: Creates thumbnails with various styles and overlays
- **content_processor.py**: Orchestrates the entire content generation process
- **ui.py**: Gradio interface for user interaction
- **main.py**: Entry point that launches the application
- **📱 Responsive UI**: Clean Gradio interface with side-by-side thumbnail comparison
- **📥 JSON Export**: Download complete metadata package for easy integration
- **⚡ Cloud-Based**: No GPU required - runs entirely on Hugging Face Inference API
- **🔄 Progress Tracking**: Real-time generation progress indicators

## 🚀 Live Demo

Try the app on Hugging Face Spaces: [https://huggingface.co/spaces/VikasURao/AI-Thumbnail-Metadata-Generator]

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Hugging Face account (for API access)
- Internet connection

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/Vikas-u-rao/ai-thumbnail-meta.git
cd ai-thumbnail-generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Hugging Face token (Optional but recommended)**
```bash
export HF_TOKEN="your_hugging_face_token_here"
```
Or set it as an environment variable in your system.

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:7860` to use the app

## 📋 Usage

### Basic Workflow

1. **Enter a Topic**: Type your video topic (e.g., "AI in Healthcare", "Cooking Tips")
2. **Choose Settings**:
   - **Style**: Select from 6 visual styles (Realistic, Cartoon, etc.)
   - **Text Model**: Choose between Zephyr-7B (faster) or Mistral-7B (more creative)
3. **Add Text Overlay** (Optional): 
   - Enter custom title text for thumbnails
   - Choose font style (Bold, Elegant, Clean)
4. **Generate**: Click "Generate Content" and watch the progress
5. **Review & Edit**: Modify generated metadata if needed
6. **Download**: Select your preferred thumbnail and download the complete package as JSON

### Advanced Features

- **Dual Generation**: Get both fast (SD-Turbo) and quality (SD-1.5) thumbnails
- **Style Prompting**: Each style uses carefully crafted prompts for optimal results
- **Text Overlay**: Automatically positions text with shadows for visibility
- **Metadata Export**: Complete YouTube-ready package with title, description, and tags

## 🎯 Example Topics

### Tech & AI
- "Future of Artificial Intelligence"
- "Best Programming Languages 2024"
- "Cybersecurity for Beginners"

### Lifestyle & Health
- "Morning Routine for Productivity" 
- "Healthy Meal Prep Ideas"
- "Home Workout Without Equipment"

### Business & Finance
- "Passive Income Strategies"
- "Social Media Marketing Tips"
- "Cryptocurrency Explained"

### Education & Skills
- "Learn Python in 30 Days"
- "Photography Composition Rules"
- "Public Speaking Confidence"

## 🔧 Configuration

### Hugging Face API Setup

The app uses Hugging Face Inference API for all AI generation:

**Text Models:**
- `HuggingFaceH4/zephyr-7b-beta` (Default - Fast & Reliable)
- `mistralai/Mistral-7B-Instruct-v0.2` (Creative & Detailed)

**Image Models:**
- `stabilityai/sd-turbo` (Fast generation - ~3 seconds)
- `runwayml/stable-diffusion-v1-5` (Quality generation - ~10 seconds)

### Environment Variables

```bash
HF_TOKEN=your_token_here  # Optional but recommended for rate limits
```

## 📁 Project Structure

```
ai-thumbnail-generator/
├── app.py              # Main Gradio application
├── app.yaml            # Hugging Face Spaces config
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore patterns
```

## 🚀 Deployment

### Hugging Face Spaces (Recommended)

1. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/spaces)
2. **Choose settings**:
   - SDK: `gradio`
   - Hardware: `CPU basic` (sufficient for API calls)
3. **Upload files** or connect your GitHub repository
4. **Set secrets** (if using authenticated API):
   - Go to Settings → Repository secrets
   - Add: `HF_TOKEN` = your_hugging_face_token
5. **Deploy**: The app will automatically build and deploy

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7860
ENV HF_TOKEN=""

CMD ["python", "app.py"]
```

### Local Development

```bash
# Development server with auto-reload
python app.py
```

## 🤖 Models & Performance

### Text Generation
- **Zephyr-7B**: ~2-3 seconds, excellent for titles and descriptions
- **Mistral-7B**: ~3-5 seconds, more creative and detailed output

### Image Generation
- **SD-Turbo**: ~3-5 seconds, good quality for rapid iteration
- **SD-1.5**: ~8-12 seconds, higher quality for final thumbnails

### Rate Limits
- **Free Tier**: ~100 requests/hour per model
- **Pro Tier**: Higher limits with HF_TOKEN authentication

## ⚠️ System Requirements

### Minimal Requirements
- **CPU**: Any modern processor
- **RAM**: 2GB available
- **Storage**: 1GB free space
- **Network**: Stable internet connection
- **Python**: 3.8+

### No GPU Required!
All processing happens on Hugging Face's cloud infrastructure.

## 🔍 Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Solution: Set up HF_TOKEN for higher limits
   - Alternative: Wait for rate limit reset

2. **Model Loading Delays**
   - Cause: Cold start on Hugging Face servers
   - Solution: Wait 10-20 seconds, models will warm up

3. **Image Generation Failures**
   - Check internet connection
   - Verify topic isn't blocked by content filters
   - Try different style options

4. **Text Overlay Issues**
   - Ensure text isn't too long (< 50 characters recommended)
   - Try different font styles
   - Check image dimensions

### Debug Mode

Set environment variable for detailed logging:
```bash
export DEBUG=1
python app.py
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Project**
2. **Create Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Make Changes** and test locally
4. **Commit Changes** (`git commit -m 'Add some AmazingFeature'`)
5. **Push to Branch** (`git push origin feature/AmazingFeature`)
6. **Open Pull Request**

### Development Setup

```bash
git clone https://github.com/Vikas-u-rao/ai-thumbnail-meta.git
cd ai-thumbnail-generator
pip install -r requirements.txt
export HF_TOKEN="your_token"
python app.py
```

## 🔄 API Reference

### Main Functions

```python
# Generate metadata
metadata = generate_metadata(topic, model_choice="zephyr")

# Generate thumbnails
thumb1, thumb2 = generate_thumbnails(topic, style, text_overlay)

# Add text overlay
image_with_text = add_text_overlay(image, title_text, style="bold")

# Create download package
json_data = create_download_data(topic, metadata, thumb1, thumb2, selected)
```


## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the amazing Inference API and model hosting
- [Gradio](https://gradio.app/) for the intuitive UI framework
- [Stability AI](https://stability.ai/) for Stable Diffusion models
- [HuggingFace H4](https://huggingface.co/HuggingFaceH4) for the Zephyr model
- [Mistral AI](https://mistral.ai/) for the Mistral language model


## 🏆 Features Roadmap

- [ ] **Batch processing for multiple topics**
- [ ] **Custom style training**
- [ ] **A/B testing for thumbnails**
- [ ] **Analytics integration**

---



