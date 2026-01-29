import streamlit as st
import requests

st.set_page_config(page_title="AI Destekli LMS")
st.title("🎓 AI Destekli LMS")
st.write("Öğrenci geri bildirimlerini yapay zeka ile analiz edin.")

feedback_text = st.text_area(
    "Öğrenci geri bildirimi girin",
    height=150
)
API_URL = "http://127.0.0.1:8000/ai/analyze-feedback"

if st.button("Analiz Et"):
    if feedback_text:
        try:
            response = requests.post(API_URL, json={"text": feedback_text, "provider": "gpt-4.1-mini"})
            result = response.json()["result"]
            st.success("Analiz Tamamlandı!")
            st.subheader("📊 AI Analiz Sonucu")
            st.write(result)
        except Exception as e:
            st.error(f"Analiz Hatası: {e}")

