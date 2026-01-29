import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Destekli LMS", page_icon="🎓")
st.title("🎓 AI Destekli LMS")
st.write("Öğrenci geri bildirimlerini yapay zeka ile analiz edin.")

# --- API ADRESİ YAPILANDIRMASI ---
is_remote = "STREAMLIT_RUNTIME_ENV" in os.environ

API_URL = "https://lms-yapayzeka-final-projesi.onrender.com/analyze-text"

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
                response = requests.post(
                    API_URL, 
                    json={"text": feedback_text, "provider": provider},
                    timeout=60 # Render ücretsiz planı uyanırken zaman gerekebilir
                )
                
                if response.status_code == 200:
                    # Backend'den gelen veriyi 'result' anahtarıyla alıyoruz
                    data = response.json()
                    result = data.get("result")
                    
                    if isinstance(result, dict) and result.get("error"):
                        st.error(f"AI Hatası: {result['error']}")
                    else:
                        st.success("Analiz Tamamlandı!")
                        st.subheader("📊 AI Analiz Sonucu")
                        st.info(result)
                else:
                    st.error(f"Sunucu Hatası: {response.status_code}")
                    st.warning(f"Bağlanmaya çalışılan adres: {API_URL}")
            
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
                if is_remote:
                    st.info("⚠️ Backend (Render) şu an uyanıyor olabilir, lütfen 30 saniye sonra tekrar deneyin.")
    else:
        st.warning("Lütfen analiz edilecek bir metin girin.")

st.divider()
st.caption(f"Şu anki mod: {'Bulut (Production)' if is_remote else 'Yerel (Development)'}")
