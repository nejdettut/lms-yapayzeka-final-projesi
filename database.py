import sqlite3
import os
from datetime import datetime

# Veritabanı dosyasının yolu
DB_PATH = "lms.db"

def get_connection():
    """
    SQLite veritabanına güvenli bir bağlantı oluşturur.
    check_same_thread=False: Streamlit gibi çoklu iş parçacığı (multi-thread) 
    çalışan yapılarda hata almamızı engeller.
    """
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        # Verileri sözlük (dictionary) yapısında alabilmek için:
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

def init_db():
    """
    Uygulama ilk başladığında tabloları ve gerekli indeksleri oluşturur.
    """
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        
        # 1. Analiz Sonuçları Tablosu
        # original_text: Öğrencinin girdiği ham metin
        # ai_result: Yapay zekanın döndüğü analiz sonucu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                original_text TEXT NOT NULL,
                ai_result TEXT NOT NULL,
                provider TEXT NOT NULL,
                sentiment_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Hızlı sorgulama için tarih indeksi ekleyelim
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON feedback_analysis(created_at)
        ''')
        
        conn.commit()
        conn.close()
        print("Veritabanı başarıyla optimize edildi ve hazırlandı.")

def save_analysis(user_name: str, text: str, result: str, provider: str):
    """
    AI analiz çıktısını veritabanına güvenli bir şekilde kaydeder.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO feedback_analysis (user_name, original_text, ai_result, provider)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query, (user_name, text, result, provider))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Veri kaydetme hatası: {e}")
        finally:
            conn.close()

def get_history(limit: int = 50):
    """
    Geçmiş analizleri en yeniden en eskiye doğru getirir.
    Limit parametresi ile performans yönetimi yapılır.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Sonuçları Row objesi olarak döner (app.py'da dict gibi kullanılır)
            cursor.execute('''
                SELECT * FROM feedback_analysis 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Veri çekme hatası: {e}")
            return []
        finally:
            conn.close()
    return []

def delete_analysis(analysis_id: int):
    """
    Belirli bir analizi ID üzerinden siler (İsteğe bağlı yönetim özelliği).
    """
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM feedback_analysis WHERE id = ?", (analysis_id,))
        conn.commit()
        conn.close()