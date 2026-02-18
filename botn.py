import os
import telebot
import google.generativeai as genai

# جلب المفاتيح من إعدادات السيرفر (Environment Variables)
CH_TOKEN = os.getenv("CH_TOKEN")
CH_GEMINI_KEY = os.getenv("CH_GEMINI_KEY")

# إعداد البوت والذكاء الاصطناعي باستخدام المتغيرات الصحيحة
bot = telebot.TeleBot(CH_TOKEN)
genai.configure(api_key=CH_GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        # أمر ذكي للترجمة بناءً على اللغة المكتوبة
        prompt = f"Translate this text: '{message.text}'. If it's Arabic, translate to English. If it's English or any other language, translate to Arabic. Keep it natural."
        
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "عذراً، حدث خطأ أثناء معالجة الترجمة.")

print("Bot is running...")
bot.polling()
