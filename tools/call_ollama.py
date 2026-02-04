import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'codellama')

def call_ollama(prompt, system_prompt="You are a code conversion expert."):
    """
    Sends a prompt to the Ollama API using CodeLlama.
    """
    url = f"{OLLAMA_API_URL}/api/generate"
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.1,  # Keep it deterministic for code
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get('response', '')
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Quick test
    test_prompt = "Convert to Playwright: driver.findElement(By.name('login')).click();"
    print(call_ollama(test_prompt))
