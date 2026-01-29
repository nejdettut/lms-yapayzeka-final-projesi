from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    # Render (Üretim) ortamı için
    from backend.models import TextRequest
    from backend.ai_service import AIService
except ImportError:
    # Yerel geliştirme ortamı için
    from models import TextRequest
    from ai_service import AIService

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



