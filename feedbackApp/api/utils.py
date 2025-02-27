import google.generativeai as genai
import pandas as pd
import logging
from django.conf import settings

# 📌 Logger Ayarları
logger = logging.getLogger(__name__)

# 📌 Gemini API Anahtarını Ayarla
#genai.configure(api_key=settings.GEMINI_API_KEY)

# 📌 Duygu Analizi Fonksiyonu (Gemini API Kullanarak)
def analyze_sentiment(comment):
    """
    Kullanıcının geri bildirimini alıp Gemini API ile duygu analizi yapar.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Bu yorumu analiz et ve sadece 'Olumlu', 'Nötr' veya 'Olumsuz' olarak cevap ver: {comment}")
        sentiment = response.text.strip()

        # Eğer API yanıtı beklenmeyen bir değer döndürürse, 'Nötr' olarak varsayalım
        if sentiment not in ["Olumlu", "Nötr", "Olumsuz"]:
            sentiment = "Nötr"
        
        return sentiment
    except Exception as e:
        logger.error(f"Gemini API çağrısında hata oluştu: {str(e)}")
        return "Nötr"

# 📌 Excel'den Yemek Verilerini Alma
def process_meal_excel(file_path):
    """
    Yöneticinin yüklediği Excel dosyasını okuyup yemek verilerini döndürür.
    """
    try:
        df = pd.read_excel(file_path)

        # 📌 Gerekli sütunlar var mı kontrol et
        required_columns = ['name', 'category', 'city', 'date']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Excel dosyasında eksik sütunlar var!")

        meals = []
        for _, row in df.iterrows():
            meals.append({
                "name": row['name'],
                "category": row['category'],
                "city": row['city'],
                "date": row['date'],
            })

        return meals
    except Exception as e:
        logger.error(f"Excel işleme hatası: {str(e)}")
        return None
