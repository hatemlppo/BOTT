import os
import telebot
import time
from google import genai

# جلب المفاتيح من إعدادات Railway
CH_TOKEN = os.getenv("CH_TOKEN")
CH_GEMINI_KEY = os.getenv("CH_GEMINI_KEY")

# إعداد البوت والذكاء الاصطناعي
bot = telebot.TeleBot(CH_TOKEN)
client = genai.Client(api_key=CH_GEMINI_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ أهلاً بك! أنا بوت الترجمة الذكي. أرسل لي أي نص وسأترجمه لك فوراً.")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        # صياغة الأمر للموديل المستقر 1.5
        prompt = f"Translate the following text. If it's Arabic, translate to English. If it's English, translate to Arabic: {message.text}"
        
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        bot.reply_to(message, response.text)
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            bot.reply_to(message, "⚠️ الخدمة مزدحمة حالياً (طلبك تجاوز الحد المجاني لدقيقة واحدة). يرجى الانتظار 30 ثانية والمحاولة مجدداً.")
        elif "404" in error_msg:
            bot.reply_to(message, "❌ خطأ في إعدادات الموديل، يرجى التأكد من استخدام gemini-1.5-flash.")
        else:
            print(f"Error details: {e}")
            bot.reply_to(message, "❌ حدث خطأ فني غير متوقع. حاول مرة أخرى لاحقاً.")

print("Bot is running perfectly on Gemini 1.5 Flash...")
bot.polling(none_stop=True)
