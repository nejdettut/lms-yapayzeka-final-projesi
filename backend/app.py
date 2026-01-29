from fastapi import FastAPI
from ai_service import analyze_text_with_llm
from models import TextRequest

app = FastAPI()

@app.post("/analyze-text")
def analyze_text_endpoint(data: TextRequest):
    result = analyze_text_with_llm(text=data.text, provider=data.provider)
    return {"result": result}