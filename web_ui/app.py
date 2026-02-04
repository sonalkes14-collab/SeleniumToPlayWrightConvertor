from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os

# Add the parent directory to sys.path so we can import our tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.call_ollama import call_ollama

app = FastAPI(title="Blast Converter API")

# Mount the static files (UI)
app.mount("/static", StaticFiles(directory="web_ui"), name="static")

class ConversionRequest(BaseModel):
    code: str

@app.get("/")
async def read_index():
    return FileResponse("web_ui/index.html")

@app.post("/convert")
async def convert(request: ConversionRequest):
    system_prompt = (
        "You are an expert Selenium-to-Playwright converter. "
        "CONVERT ONLY THE LOGIC inside the Java method. "
        "DO NOT include 'test(...)', 'await context.newPage()', or 'import' statements. "
        "DO NOT include ANY markdown formatting like ```typescript. "
        "ONLY PROVIDE THE JS/TS STATEMENTS. "
        "Assume the 'page' object is already available."
    )
    
    try:
        converted_code = call_ollama(request.code, system_prompt)
        
        # Robust stripping of LLM fluff (same logic as main_coordinator)
        if "```" in converted_code:
            parts = converted_code.split("```")
            if len(parts) >= 3:
                converted_code = parts[1].strip()
                if converted_code.startswith("typescript"):
                    converted_code = converted_code[len("typescript"):].strip()
                elif converted_code.startswith("ts"):
                    converted_code = converted_code[len("ts"):].strip()
            else:
                converted_code = parts[-1].strip()
        
        converted_code = converted_code.strip()
        return {"result": converted_code}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
