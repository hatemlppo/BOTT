import os
import telebot
from google import genai
from google.genai import types

# جلب المفاتيح من إعدادات Railway
CH_TOKEN = os.getenv("CH_TOKEN")
CH_GEMINI_KEY = os.getenv("CH_GEMINI_KEY")

# إعداد البوت والذكاء الاصطناعي
bot = telebot.TeleBot(CH_TOKEN)
client = genai.Client(api_key=CH_GEMINI_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ أهلاً بك! أنا بوت الترجمة الذكي.\nأرسل لي أي نص وسأقوم بترجمته فوراً (عربي ↔️ إنجليزي).")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        # صياغة الأمر للموديل
        prompt = f"You are a professional translator. Translate the following text to Arabic if it's English, and to English if it's Arabic: {message.text}"
        
        # الطريقة الأكثر استقراراً في 2026 لاستدعاء الموديل
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3, # لجعل الترجمة أكثر دقة وأقل إبداعاً
            )
        )

        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "⚠️ لم أتمكن من استخراج ترجمة للنص.")

    except Exception as e:
        error_msg = str(e)
        print(f"Detailed Error: {error_msg}")
        
        if "429" in error_msg:
            bot.reply_to(message, "⚠️ الطلبات كثيرة حالياً. انتظر دقيقة وجرب مجدداً.")
        else:
            # محاولة أخيرة باستخدام موديل بديل إذا فشل 1.5
            try:
                response = client.models.generate_content(model="gemini-1.5-pro", contents=prompt)
                bot.reply_to(message, response.text)
            except:
                bot.reply_to(message, "❌ حدث خطأ فني. تأكد من شحن رصيد الـ API أو صحة المفتاح.")

print("Bot is live on Railway...")
bot.polling(none_stop=True)
