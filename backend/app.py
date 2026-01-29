from fastapi import FastAPI
from models import TextRequest
from fastapi.middleware.cors import CORSMiddleware
try:
    from backend import models, ai_service, database
except ImportError:
    import models, ai_service, database

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


