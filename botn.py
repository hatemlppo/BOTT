import os
import telebot
from deep_translator import GoogleTranslator

# جلب توكن التليجرام فقط
CH_TOKEN = os.getenv("CH_TOKEN")

# إعداد البوت
bot = telebot.TeleBot(CH_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ أهلاً بك! أنا بوت ترجمة سريع ومجاني.\nأرسل لي أي نص وسأترجمه تلقائياً (عربي ↔️ إنجليزي).")

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    try:
        text = message.text
        # تحديد المترجم: إذا كان النص عربي يترجمه لإنجليزي، والعكس صحيح
        # سنستخدم مكتبة لاكتشاف اللغة أو ببساطة الترجمة الآلية
        
        translator = GoogleTranslator(source='auto', target='en' if not any('\u0600' <= c <= '\u06FF' for c in text) else 'ar')
        
        # إذا كان النص يحتوي على حروف عربية، نترجمه للإنجليزية
        if any('\u0600' <= c <= '\u06FF' for c in text):
            translated = GoogleTranslator(source='ar', target='en').translate(text)
        else:
            # إذا كان النص إنجليزي، نترجمه للعربية
            translated = GoogleTranslator(source='en', target='ar').translate(text)

        bot.reply_to(message, translated)

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ عذراً، حدث خطأ أثناء الترجمة.")

print("Offline Translation Bot is running...")
bot.polling(none_stop=True)
