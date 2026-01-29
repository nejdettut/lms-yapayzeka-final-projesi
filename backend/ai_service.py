import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

try:
    from groq import Groq
except ImportError:
    Groq = None

# .env proje kökünde (backend'in bir üst klasörü)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

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
    if Groq is None:
        return {"error": "Groq paketi yüklü değil. pip install groq", "api_configured": False}
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "Groq API Key bulunamadı! .env içinde GROQ_API_KEY tanımlayın.", "api_configured": False}
    
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


def analyze_text_with_llm(text: str, provider: str = "gemini"):
    """provider: 'gemini' veya 'groq'"""
    if provider and provider.lower() == "groq":
        return analyze_with_groq(text)
    return analyze_with_gemini(text)
