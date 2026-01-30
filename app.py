import streamlit as st
from ai_service import analyze_text
from database import init_db, save_analysis, get_history
from models import TextRequest

# 1. Başlangıç Ayarları
st.set_page_config(page_title="AI Destekli LMS", page_icon="🎓")

# Uygulama açıldığında veritabanı tablolarını oluştur (Eğer yoksa)
init_db()

st.title("🎓 AI Destekli LMS Analiz Paneli")
st.markdown("---")

# 2. Yan Menü (Sekme Mantığı)
menu = st.sidebar.selectbox("Menü", ["Analiz Yap", "Geçmiş Analizler"])

if menu == "Analiz Yap":
    st.subheader("📝 Yeni Analiz")
    
    # Kullanıcı Girdileri
    user_name = st.text_input("Kullanıcı Adınız", value="Öğrenci")
    feedback_text = st.text_area("Analiz edilecek geri bildirimi girin:", height=150)
    provider = st.selectbox("AI Modeli", ["gemini", "groq"])

    if st.button("AI Analizini Başlat"):
        if feedback_text:
            with st.spinner("Yapay zeka analiz ediyor..."):
                try:
                    # A. Veri Doğrulama (Models kullanımı)
                    request_data = TextRequest(text=feedback_text, provider=provider)
                    
                    # B. AI Servis Çağrısı
                    response = analyze_text(request_data.text, request_data.provider)
                    
                    if "error" in response:
                        st.error(response["error"])
                    else:
                        # C. Sonuçları Ekranda Göster
                        st.success("Analiz Tamamlandı!")
                        st.markdown(f"**Kaynak:** {response['source']}")
                        st.info(response["analysis"])
                        
                        # D. Veritabanına Kaydet (Database kullanımı)
                        save_analysis(
                            user_name=user_name,
                            text=feedback_text,
                            result=response["analysis"],
                            provider=response["source"]
                        )
                        st.toast("Veritabanına kaydedildi!")
                        
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen bir metin girin.")

elif menu == "Geçmiş Analizler":
    st.subheader("📜 Analiz Geçmişi")
    history = get_history()
    
    if not history:
        st.write("Henüz bir analiz kaydı bulunamadı.")
    else:
        for row in history:
            with st.expander(f"📌 {row['user_name']} - {row['created_at']}"):
                st.write(f"**Orijinal Metin:** {row['original_text']}")
                st.write(f"**AI Analizi:** {row['ai_result']}")
                st.caption(f"Model: {row['provider']}")

st.markdown("---")
st.caption("LMS AI Final Project v1.0")