import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

load_dotenv()

# --- Google Gemini Ayarları ---
def analyze_with_gemini(text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "Gemini API Key bulunamadı!", "api_configured": False}
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Şu metni analiz et ve kısa özetle: {text}")
        return {
            "source": "Google Gemini",
            "analysis": response.text,
            "api_configured": True
        }
    except Exception as e:
        return {"error": str(e), "api_configured": False}

# --- Groq Cloud Ayarları ---
def analyze_with_groq(text):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "Groq API Key bulunamadı!", "api_configured": False}
    
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Aşağıdaki metni analiz et: {text}"}]
        )
        return {
            "source": "Groq (Llama 3)",
            "analysis": completion.choices[0].message.content,
            "api_configured": True
        }
    except Exception as e:
        return {"error": str(e), "api_configured": False}


SYSTEM_PROMPT = """
Sen bir eğitim platformunda çalışan yapay zeka asistanısın.
Görevin, öğrenci geri bildirimlerini analiz etmek.
Analiz sonucunda:
- Kısa özet
- Duygu durumu
- Eğitmen için öneri
üret.
"""

def analyze_text_with_llm(text: str):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


