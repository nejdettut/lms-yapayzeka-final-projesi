from pydantic import BaseModel, Field, validator
from typing import Optional

class TextRequest(BaseModel):
    """
    Kullanıcıdan gelen analiz isteğini doğrular.
    """
    # text alanının en az 5 karakter olmasını zorunlu kılıyoruz
    text: str = Field(
        ..., 
        min_length=5, 
        max_length=5000,
        description="Analiz edilecek öğrenci geri bildirimi"
    )
    
    # provider alanının varsayılan değeri 'gemini'
    provider: str = Field(
        default="gemini", 
        description="Kullanılacak yapay zeka modeli (gemini veya groq)"
    )

    # Örnek bir validator: Sadece izin verilen modellerin girilmesini sağlar
    @validator('provider')
    def provider_must_be_supported(cls, v):
        allowed = ['gemini', 'groq']
        if v.lower() not in allowed:
            raise ValueError(f"Desteklenmeyen model: {v}. Lütfen 'gemini' veya 'groq' seçin.")
        return v.lower()

class AnalysisResponse(BaseModel):
    """
    AI servisinden dönen sonucun standart yapısı (Opsiyonel kullanım için).
    """
    source: str
    analysis: str
    status: str = "success"
    error_details: Optional[str] = None