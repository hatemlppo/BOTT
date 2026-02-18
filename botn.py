import os
import telebot
from google import genai # المكتبة الجديدة لعام 2026

# جلب المفاتيح
CH_TOKEN = os.getenv("CH_TOKEN")
CH_GEMINI_KEY = os.getenv("CH_GEMINI_KEY")

# إعداد البوت والذكاء الاصطناعي
bot = telebot.TeleBot(CH_TOKEN)
client = genai.Client(api_key=CH_GEMINI_KEY) # الطريقة الجديدة للتعريف

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        # استخدام موديل gemini-2.0-flash (الأحدث والأكثر استقراراً في 2026)
        prompt = f"Translate to Arabic if English, and vice versa: {message.text}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "عذراً، حدث خطأ في الترجمة. جرب مرة أخرى.")

print("Bot is running perfectly on Railway...")
bot.polling()
