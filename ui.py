import gradio as gr
import json
from config import STYLE_PROMPTS, current_hf_token, current_openrouter_token
from api_utils import test_hf_token
from content_processor import process_content


def create_gradio_ui():
    """Create and return the Gradio interface"""
    with gr.Blocks(title="AI Thumbnail & Metadata Generator", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        ## 🔑 API Key Management
        **⚠️ Important:**
        - You need a valid OpenRouter API key for text generation (metadata).
        - You need a valid Hugging Face API key for image generation (thumbnails).
        
        Get your OpenRouter API key at [https://openrouter.ai/](https://openrouter.ai/) (sign up and generate your key)
        Get your Hugging Face API key at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
        """)
        with gr.Row():
            openrouter_token_input = gr.Textbox(label="OpenRouter API Key", placeholder="Paste your OpenRouter API key here", value="", type="password")
            set_openrouter_token_btn = gr.Button("Set OpenRouter Key", variant="primary")
            clear_openrouter_token_btn = gr.Button("Clear OpenRouter Key", variant="secondary")
            test_openrouter_token_btn = gr.Button("Test OpenRouter Key", variant="secondary")
        openrouter_token_status = gr.Textbox(label="OpenRouter Key Status", interactive=False)

        with gr.Row():
            hf_token_input = gr.Textbox(label="Hugging Face API Key", placeholder="Paste your Hugging Face API key here", value="", type="password")
            set_hf_token_btn = gr.Button("Set HF Key", variant="primary")
            clear_hf_token_btn = gr.Button("Clear HF Key", variant="secondary")
            test_hf_token_btn = gr.Button("Test HF Key", variant="secondary")
        hf_token_status = gr.Textbox(label="HF Key Status", interactive=False)

        # Store keys separately
        def set_openrouter_token_callback(token):
            global current_openrouter_token
            current_openrouter_token = token.strip()
            return "✅ OpenRouter API key set!"

        def clear_openrouter_token_callback():
            global current_openrouter_token
            current_openrouter_token = ""
            return "🗑️ OpenRouter API key cleared."

        def set_hf_token_callback(token):
            global current_hf_token
            current_hf_token = token.strip()
            return "✅ Hugging Face API key set!"

        def clear_hf_token_callback():
            global current_hf_token
            current_hf_token = ""
            return "🗑️ Hugging Face API key cleared."

        set_openrouter_token_btn.click(fn=set_openrouter_token_callback, inputs=openrouter_token_input, outputs=openrouter_token_status)
        clear_openrouter_token_btn.click(fn=clear_openrouter_token_callback, inputs=None, outputs=openrouter_token_status)
        test_openrouter_token_btn.click(fn=lambda k: "✅ Key format looks valid!" if k and len(k) > 10 else "❌ Please enter a valid OpenRouter API key.", inputs=openrouter_token_input, outputs=openrouter_token_status)

        set_hf_token_btn.click(fn=set_hf_token_callback, inputs=hf_token_input, outputs=hf_token_status)
        clear_hf_token_btn.click(fn=clear_hf_token_callback, inputs=None, outputs=hf_token_status)
        test_hf_token_btn.click(fn=test_hf_token, inputs=hf_token_input, outputs=hf_token_status)
        
        gr.Markdown("""
        # 🎨 AI Thumbnail & Metadata Generator
        
        Generate catchy YouTube titles, descriptions, tags, and stunning thumbnails using AI models!
        
        **✨ Features:**
        - 🤖 AI-powered metadata generation
        - 🎨 Dual thumbnail generation (Fast & Quality)
        - 🎯 6 different visual styles
        - ✏️ Custom text overlay editor
        - 📥 Download metadata as JSON
        
        **How to use:**
        1. Enter your video topic
        2. Choose thumbnail style and text model
        3. Add custom text overlay (optional)
        4. Generate content and download!
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("### 📝 Input Settings")
                
                topic_input = gr.Textbox(
                    label="Video Topic",
                    placeholder="e.g., AI in Healthcare, Cooking Tips, Travel Photography...",
                    lines=2
                )
                
                with gr.Row():
                    style_dropdown = gr.Dropdown(
                        choices=list(STYLE_PROMPTS.keys()),
                        value="Realistic",
                        label="Thumbnail Style"
                    )
                    
                    model_dropdown = gr.Dropdown(
                        choices=["deepseek-r1-free"],
                        value="deepseek-r1-free",
                        label="Text Model"
                    )
                
                gr.Markdown("### ✏️ Text Overlay (Optional)")
                
                text_overlay_input = gr.Textbox(
                    label="Custom Title Text",
                    placeholder="Leave empty to use generated title...",
                    lines=2
                )
                
                overlay_style_dropdown = gr.Dropdown(
                    choices=["bold", "elegant", "clean"],
                    value="bold",
                    label="Text Style"
                )
                
                generate_btn = gr.Button("🚀 Generate Content", variant="primary", size="lg")
                
                # Metadata section
                gr.Markdown("### 📋 Generated Metadata")
                metadata_output = gr.Textbox(
                    label="YouTube Title, Description & Tags",
                    lines=8,
                    placeholder="Generated metadata will appear here...",
                    info="✏️ Edit this text before using it for your video!"
                )
                
                # Download section - simplified
                gr.Markdown("### 📥 Export Data")
                export_output = gr.Textbox(
                    label="📋 Copy this JSON data",
                    lines=5,
                    placeholder="JSON export will appear here...",
                    info="Copy this data to save your metadata"
                )
                
                download_data = gr.Textbox(
                    label="Metadata JSON",
                    lines=3,
                    placeholder="JSON data will appear here...",
                    visible=False
                )
        
            with gr.Column(scale=2):
                # Thumbnails section
                gr.Markdown("### 🖼️ Generated Thumbnails")
                
                with gr.Row():
                    thumbnail1_output = gr.Image(
                        label="🚀 Fast Generation (FLUX.1-schnell)",
                        type="pil",
                        show_download_button=True
                    )
                    thumbnail2_output = gr.Image(
                        label="💎 Quality Generation (FLUX.1-dev)", 
                        type="pil",
                        show_download_button=True
                    )
                
                # Thumbnail selection for JSON export
                with gr.Row():
                    select_thumb1_btn = gr.Button("📥 Use Fast Thumbnail", size="sm")
                    select_thumb2_btn = gr.Button("📥 Use Quality Thumbnail", size="sm")
    
        # Event handlers
        generate_btn.click(
            fn=process_content,
            inputs=[topic_input, style_dropdown, model_dropdown, text_overlay_input, overlay_style_dropdown],
            outputs=[metadata_output, thumbnail1_output, thumbnail2_output, download_data]
        )
        
        # Thumbnail selection for export
        def update_export_data(topic, metadata, download_data, selected):
            if download_data:
                try:
                    data = json.loads(download_data)
                    data["selected_thumbnail"] = selected
                    return json.dumps(data, indent=2)
                except Exception as e:
                    print(f"Export error: {e}")
                    return f"Error creating export: {e}"
            return ""
        
        select_thumb1_btn.click(
            fn=lambda t, m, d: update_export_data(t, m, d, "fast_thumbnail"),
            inputs=[topic_input, metadata_output, download_data],
            outputs=[export_output]
        )
        
        select_thumb2_btn.click(
            fn=lambda t, m, d: update_export_data(t, m, d, "quality_thumbnail"),
            inputs=[topic_input, metadata_output, download_data],
            outputs=[export_output]
        )
        
        # Example inputs
        gr.Markdown("""
        ### 💡 Example Topics to Try:
        
        **Tech & AI:**
        - "Future of Artificial Intelligence"
        - "Best Programming Languages 2024"
        - "Cybersecurity for Beginners"
        
        **Lifestyle & Health:**
        - "Morning Routine for Productivity"
        - "Healthy Meal Prep Ideas"
        - "Home Workout Without Equipment"
        
        **Business & Finance:**
        - "Passive Income Strategies"
        - "Social Media Marketing Tips"
        - "Cryptocurrency Explained"
        
        **Education & Skills:**
        - "Learn Python in 30 Days"
        - "Photography Composition Rules"
        - "Public Speaking Confidence"
        """)

    return app