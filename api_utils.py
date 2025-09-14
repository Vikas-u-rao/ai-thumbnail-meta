import requests
import time
from config import current_hf_token


def test_hf_token(token):
    """Test Hugging Face token by calling the user endpoint"""
    if not token or not token.strip():
        return "❌ Please enter a token first"
    
    url = "https://huggingface.co/api/whoami-v2"
    headers = {"Authorization": f"Bearer {token.strip()}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            user_name = data.get('name', 'unknown')
            
            # Test inference providers access
            test_url = "https://router.huggingface.co/v1/models"
            test_resp = requests.get(test_url, headers=headers, timeout=10)
            
            if test_resp.status_code == 200:
                return f"✅ Token valid! User: {user_name} - Inference Providers access confirmed!"
            else:
                return f"⚠️ Token valid for user {user_name}, but may lack Inference Providers permissions. Check token settings."
        elif resp.status_code == 401:
            return "❌ Invalid token. Please check and try again."
        else:
            return f"❌ Error: {resp.status_code} {resp.text[:100]}"
    except Exception as e:
        return f"❌ Connection error: {e}"


def query_hf_api(api_url, payload, max_retries=3):
    """Query Hugging Face Inference API with retries"""
    global current_hf_token
    token = current_hf_token
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    print(f"🔄 Calling API: {api_url}")
    print(f"🔑 Using Hugging Face token: {'Yes' if token else 'No (public access)'}")
    
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ API call successful!")
                return response
            elif response.status_code == 404:
                print(f"❌ Model not found (404). Model may not be available.")
                break  # Don't retry 404 errors
            elif response.status_code == 503:
                print(f"⏳ Model loading, waiting... (attempt {attempt + 1})")
                time.sleep(15)
            elif response.status_code == 429:
                print(f"⏱️ Rate limited, waiting... (attempt {attempt + 1})")
                time.sleep(20)
            elif response.status_code == 401:
                print(f"🔐 Authentication error. Check your token.")
                break  # Don't retry auth errors
            else:
                print(f"❌ API Error {response.status_code}: {response.text[:500]}")
                time.sleep(5)
        except Exception as e:
            print(f"❌ Request failed (attempt {attempt + 1}): {e}")
            time.sleep(5)
    
    print("💥 All API attempts failed!")
    return None