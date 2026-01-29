from fastapi import Body, FastAPI
from ai_service import analyze_text_with_llm

app = FastAPI()

@app.post("/analyze-text")
def analyze_text_endpoint(data: TextRequest):
    # Fonksiyona kullanıcıdan gelen provider bilgisini gönderiyoruz
    result = ai_service.analyze_text_with_llm(
        text=data.text, 
        provider=data.provider # "gemini" veya "groq"
    )
    return {"result": result}