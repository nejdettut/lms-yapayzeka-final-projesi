from fastapi import FastAPI
from ai_service import analyze_text_with_llm
from models import TextRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Ayarları: Streamlit'ten gelen isteklere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için daha sonra Streamlit URL'nizi buraya yazabilirsiniz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-text")
async def analyze(data: dict):
    # Analiz kodlarınız...
    return {"result": "Başarılı"}
