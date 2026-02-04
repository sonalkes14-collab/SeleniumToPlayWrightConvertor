"""
Ollama API Connection Test
Tests connectivity to Ollama API and verifies CodeLlama model availability
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'codellama')

def test_ollama_connection():
    """Test if Ollama API is accessible"""
    print("--- Testing Ollama API connection...")
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print("[SUCCESS] Ollama API is accessible")
            return True
        else:
            print(f"[FAILURE] Ollama API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[FAILURE] Cannot connect to Ollama at {OLLAMA_API_URL}")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"[FAILURE] Error connecting to Ollama: {e}")
        return False

def test_model_availability():
    """Test if CodeLlama model is available"""
    print(f"\n--- Checking if model '{OLLAMA_MODEL}' is available...")
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            print(f"   Available models: {models}")
            
            # Check for exact match or partial match
            model_found = any(OLLAMA_MODEL in model for model in models)
            
            if model_found:
                print(f"[SUCCESS] Model '{OLLAMA_MODEL}' is available")
                return True
            else:
                print(f"[FAILURE] Model '{OLLAMA_MODEL}' not found")
                print(f"   Run: ollama pull {OLLAMA_MODEL}")
                return False
        return False
    except Exception as e:
        print(f"[FAILURE] Error checking model: {e}")
        return False

def test_model_inference():
    """Test a simple inference with CodeLlama"""
    print(f"\n--- Testing inference with {OLLAMA_MODEL}...")
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": "Convert this Selenium Java code to Playwright TypeScript: driver.findElement(By.id(\"btn\")).click();",
            "stream": False
        }
        
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("[SUCCESS] Model inference successful")
            print(f"   Response preview: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"[FAILURE] Inference failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAILURE] Error during inference: {e}")
        return False

def main():
    """Run all connectivity tests"""
    print("=" * 60)
    print("PHASE 2: LINK - Ollama Connectivity Test")
    print("=" * 60)
    
    results = {
        'connection': test_ollama_connection(),
        'model': False,
        'inference': False
    }
    
    if results['connection']:
        results['model'] = test_model_availability()
        
        if results['model']:
            results['inference'] = test_model_inference()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS:")
    print("=" * 60)
    print(f"API Connection:    {'PASS' if results['connection'] else 'FAIL'}")
    print(f"Model Available:   {'PASS' if results['model'] else 'FAIL'}")
    print(f"Inference Test:    {'PASS' if results['inference'] else 'FAIL'}")
    print("=" * 60)
    
    if all(results.values()):
        print("\nAll tests passed! Ollama link is ready.")
        return True
    else:
        print("\nSome tests failed. Fix issues before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
