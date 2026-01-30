import os
import streamlit as st
from dotenv import load_dotenv

# Yapay zeka kütüphaneleri
import google.generativeai as genai
try:
    from groq import Groq
except ImportError:
    Groq = None

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# Profesyonel Sistem Komutu
SYSTEM_PROMPT = """
Sen bir Eğitim Teknolojileri (EdTech) uzmanısın. 
Görevin, öğrencilerin dersler hakkındaki geri bildirimlerini analiz etmektir.
Lütfen analizi şu başlıklarla sun:
1. Genel Duygu Analizi (Pozitif / Negatif / Karışık)
2. Öne Çıkan Şikayetler veya Beğeniler (Kısa Maddelerle)
3. Eğitmen İçin Aksiyon Planı (Dersi iyileştirmek için ne yapmalı?)
Daima nazik ve yapıcı bir dil kullan.
"""

def analyze_text(text: str, provider: str = "gemini"):
    gemini_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

    if provider.lower() == "gemini":
        if not gemini_key: return {"error": "Gemini API Key eksik."}
        
        try:
            genai.configure(api_key=gemini_key)
            
            # --- ZEKİ MODEL SEÇİMİ ---
            # Hesabındaki aktif modelleri listele ve en yeni 'flash' modelini bul
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Tercih sırası: 2.5 Flash -> 2.0 Flash -> 1.5 Flash
            target_model = None
            for m_name in ["models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-1.5-flash"]:
                if m_name in available_models:
                    target_model = m_name
                    break
            
            # Eğer hiçbiri bulunamazsa listedeki ilk uygun modeli al
            if not target_model:
                target_model = available_models[0] if available_models else "models/gemini-pro"

            model = genai.GenerativeModel(target_model)
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nMetin: {text}")
            
            return {
                "source": f"Google {target_model.split('/')[-1]}",
                "analysis": response.text
            }
        except Exception as e:
            return {"error": f"Gemini Hatası: {str(e)}"}

    elif provider.lower() == "groq":
        # Groq kısmına dokunmuyoruz, çalıştığını biliyoruz
        if not groq_key: return {"error": "Groq API Key eksik."}
        try:
            client = Groq(api_key=groq_key)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}],
                model="llama-3.1-8b-instant", 
                temperature=0.7
            )
            return {"source": "Groq Llama 3.1", "analysis": chat_completion.choices[0].message.content}
        except Exception as e:
            return {"error": f"Groq Hatası: {str(e)}"}

    return {"error": "Geçersiz sağlayıcı."}