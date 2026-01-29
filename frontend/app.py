import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Destekli LMS", page_icon="🎓")
st.title("🎓 AI Destekli LMS")
st.write("Öğrenci geri bildirimlerini yapay zeka ile analiz edin.")

# --- API ADRESİ YAPILANDIRMASI ---
# Uygulama Streamlit Cloud'da mı çalışıyor kontrol et
is_remote = "STREAMLIT_RUNTIME_ENV" in os.environ

if is_remote:
    # BURAYA: FastAPI'yi Render/Railway'e yükleyince aldığın URL'yi yazacaksın
    API_URL = "https://lms-yapayzeka-final-projesi.onrender.com/analyze-text"
else:
    # Kendi bilgisayarında çalışırken kullanılacak adres
    API_URL = "http://127.0.0.1:8000/analyze-text"

# --- ARAYÜZ ---
feedback_text = st.text_area(
    "Öğrenci geri bildirimi girin",
    height=150,
    placeholder="Örn: Dersin anlatımı çok iyiydi ancak örnekler yetersizdi..."
)

provider = st.selectbox("AI Sağlayıcı Seçin", ["gemini", "groq"], index=0)

if st.button("Analiz Et"):
    if feedback_text:
        with st.spinner(f"{provider.capitalize()} ile analiz ediliyor..."):
            try:
                # Backend'e (FastAPI) istek gönderiyoruz
                response = requests.post(
                    API_URL, 
                    json={"text": feedback_text, "provider": provider},
                    timeout=30 # Zaman aşımı eklemek iyidir
                )
                
                if response.status_code == 200:
                    result = response.json().get("result")
                    
                    if isinstance(result, dict) and result.get("error"):
                        st.error(f"AI Hatası: {result['error']}")
                    else:
                        st.success("Analiz Tamamlandı!")
                        st.subheader("📊 AI Analiz Sonucu")
                        st.info(result)
                else:
                    st.error(f"Sunucu Hatası: {response.status_code}")
                    if is_remote:
                        st.warning("İpucu: Backend sunucunuzun (FastAPI) yayında olduğundan emin olun.")
            
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
                if not is_remote:
                    st.info("Not: Yerel backend sunucunuzun (port 8000) çalıştığından emin olun.")
    else:
        st.warning("Lütfen analiz edilecek bir metin girin.")

# Alt bilgi
st.divider()
st.caption(f"Şu anki mod: {'Bulut (Production)' if is_remote else 'Yerel (Development)'}")
