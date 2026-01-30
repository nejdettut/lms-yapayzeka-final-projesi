Harika bir fikir! Projenin "kod" aşamasından çıkıp gerçek bir "ürün" ve "portföy parçası" haline gelmesi için profesyonel bir **README.md** dosyası şart. Bu dosya, senin GitHub profilini ziyaret eden bir işe alım uzmanının veya yöneticinin projeni saniyeler içinde anlamasını sağlar.

İşte projenin kök dizinine eklemen gereken en ayrıntılı ve şık **README.md** içeriği:

---

# 🎓 AI Destekli LMS - Geri Bildirim Analiz Sistemi

Bu proje, Eğitim Yönetim Sistemleri (LMS) için geliştirilmiş, öğrenci geri bildirimlerini **Doğal Dil İşleme (NLP)** teknikleriyle analiz eden uçtan uca bir yapay zeka ürünüdür. Eğitmenlerin ders kalitesini artırmalarına yardımcı olmak için duygu analizi ve aksiyon önerileri sunar.

## 🚀 Öne Çıkan Özellikler

* **Çift LLM Desteği:** Kullanıcılar analiz için **Google Gemini 1.5 Flash** veya **Groq (Meta Llama 3)** modellerinden birini seçebilir.
* **Duygu ve İçerik Analizi:** Yapay zeka, metni özetler, duygu durumunu belirler ve iyileştirme önerileri sunar.
* **Veri Kalıcılığı:** Yapılan tüm analizler **SQLite** veritabanında tarih ve model bilgisiyle birlikte saklanır.
* **Gelişmiş Veri Doğrulama:** **Pydantic** modelleri ile API'ye gönderilen veriler önceden denetlenir.
* **Kullanıcı Dostu Arayüz:** **Streamlit** ile geliştirilmiş modern ve hızlı bir dashboard.

## 🛠️ Teknolojiler

* **Dil:** Python 3.9+
* **Frontend:** Streamlit
* **Backend/Logic:** Pydantic (Veri Doğrulama), python-dotenv
* **Veritabanı:** SQLite3
* **AI Entegrasyonları:** Google Generative AI SDK, Groq SDK

## 📁 Proje Yapısı

```text
ai_lms_project/
├── app.py             # Ana uygulama ve Streamlit arayüzü
├── ai_service.py      # AI model entegrasyonları (Gemini/Groq)
├── database.py        # Veritabanı işlemleri (SQLite)
├── models.py          # Pydantic veri modelleri
├── .env               # API anahtarları (Gizli)
├── .gitignore         # Gereksiz dosyaların takibini önler
└── requirements.txt   # Gerekli kütüphaneler listesi

```

## ⚙️ Kurulum ve Kullanım

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/nejdettut/lms-yapayzeka-final-projesi.git
cd ai-lms-project

```

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt

```

### 3. API Anahtarlarını Ayarlayın

Proje klasöründe `.env` adında bir dosya oluşturun ve anahtarlarınızı ekleyin:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

```

### 4. Uygulamayı Başlatın

```bash
streamlit run app.py

```

## 🔒 Güvenlik Notu

Bu projede API anahtarları asla kod içerisine gömülmemiştir. Yerel ortamda `.env` dosyası, canlı ortamda (Deploy) ise platformun kendi **Secret Manager** (Streamlit Secrets) yapısı kullanılmaktadır. `.env` dosyası `.gitignore` ile korunmaktadır.

---

**Geliştiren:** Nejdet TUT
**İletişim:** nejdetttut@gmail.com  & github.com/nejdettut
              

