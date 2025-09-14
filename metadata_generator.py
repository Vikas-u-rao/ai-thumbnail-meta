import requests
import random
import re
from config import TEXT_MODELS, OPENROUTER_API_URL, current_openrouter_token


def create_smart_fallback_metadata(topic):
    """Create smart fallback metadata when AI generation fails"""
    
    # Smart title templates
    title_templates = [
        f"Ultimate {topic} Guide",
        f"{topic} Secrets Revealed",
        f"Master {topic} in Minutes",
        f"{topic} Pro Tips & Tricks",
        f"Everything About {topic}",
        f"{topic} Made Simple",
        f"The Complete {topic} Tutorial"
    ]
    
    # Smart description templates
    desc_templates = [
        f"Learn everything you need to know about {topic} in this comprehensive guide. Perfect for beginners and experts alike!",
        f"Discover the best {topic} techniques and strategies. Transform your skills with these proven methods!",
        f"Master {topic} with this step-by-step tutorial. Get professional results every time!",
        f"Unlock the secrets of {topic}. This detailed guide covers everything from basics to advanced techniques!",
        f"The ultimate {topic} resource you've been looking for. Clear explanations and practical examples included!"
    ]
    
    # Generate relevant tags based on topic
    base_tags = [topic.lower().replace(" ", "-")]
    topic_words = topic.lower().split()
    
    common_tags = ["tutorial", "guide", "tips", "howto", "learn", "beginner", "expert", "professional"]
    selected_tags = base_tags + topic_words + random.sample(common_tags, 3)
    
    return f"""TITLE: {random.choice(title_templates)}
DESCRIPTION: {random.choice(desc_templates)}
TAGS: {", ".join(selected_tags[:7])}"""


def generate_metadata(topic, model_choice="deepseek-r1-free"):
    """Generate YouTube metadata using OpenRouter API"""
    try:
        print(f"🤖 Generating metadata with {model_choice} for: {topic}")
        model_name = TEXT_MODELS[model_choice]
        global current_openrouter_token
        if not current_openrouter_token:
            print("⚠️ No OpenRouter API key provided, using smart fallback response")
            return create_smart_fallback_metadata(topic)

        # OpenRouter expects OpenAI-style chat payload
        messages = [
            {
                "role": "user",
                "content": f"Create a YouTube title, description, and tags for a video about {topic}. Format: TITLE: [title] DESCRIPTION: [description] TAGS: [tags]"
            }
        ]
        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": 200,
            "temperature": 0.7
        }
        headers = {
            "Authorization": f"Bearer {current_openrouter_token}",
            "Content-Type": "application/json"
        }
        print(f"🔄 Calling OpenRouter API for {model_name}")
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
        print(f"📡 Response status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"📝 Raw API response: {result}")
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0]["message"]
                generated_text = message.get("content", "")
                if generated_text.strip():
                    print(f"✅ Generated text: {generated_text[:200]}...")
                    return generated_text.strip()
                # Fallback to reasoning if content is empty
                reasoning_text = message.get("reasoning", "")
                if reasoning_text.strip():
                    print(f"⚠️ Using reasoning as fallback: {reasoning_text[:200]}...")
                    # Try to extract title, description, tags from reasoning
                    title_match = re.search(r'title.*?"([^"]+)"', reasoning_text, re.IGNORECASE)
                    description_match = re.search(r'description.*?"([^"]+)"', reasoning_text, re.IGNORECASE)
                    tags_match = re.search(r'tags.*?([\w, ]+)', reasoning_text, re.IGNORECASE)
                    title = title_match.group(1) if title_match else f"{topic}: AI Insights"
                    description = description_match.group(1) if description_match else f"Explore how AI is transforming {topic}. Discover trends, breakthroughs, and real-world examples in this video."
                    tags = tags_match.group(1) if tags_match else f"ai, {topic.lower().replace(' ', '-')}, healthcare, technology, innovation"
                    formatted = f"TITLE: {title}\nDESCRIPTION: {description}\nTAGS: {tags}"
                    return formatted
                print("❌ No usable content or reasoning in response; using smart fallback.")
                return create_smart_fallback_metadata(topic)
            else:
                print("❌ No choices in response")
        elif response.status_code == 401:
            print(f"🔐 Authentication error. Invalid API key.")
        elif response.status_code == 403:
            print(f"🔐 Forbidden. API key may not have required permissions.")
        else:
            print(f"❌ API Error {response.status_code}: {response.text[:500]}")
        print("⚠️ Using smart fallback response...")
        return create_smart_fallback_metadata(topic)
    except Exception as e:
        print(f"❌ Error generating metadata: {e}")
        return create_smart_fallback_metadata(topic)