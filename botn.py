import os
import telebot
from deep_translator import GoogleTranslator

# جلب توكن التليجرام فقط
CH_TOKEN = os.getenv("CH_TOKEN")

# إعداد البوت
bot = telebot.TeleBot(CH_TOKEN)

# معرف القناة المطلوب الاشتراك فيها
REQUIRED_CHANNEL = "@THTOMI"

def check_subscription(user_id):
    """التحقق من اشتراك المستخدم في القناة"""
    try:
        member = bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Subscription check error: {e}")
        return False

def subscription_required(func):
    """ديكوريتور للتحقق من الاشتراك قبل تنفيذ أي أمر"""
    def wrapper(message):
        user_id = message.from_user.id
        if not check_subscription(user_id):
            # إنشاء رابط القناة
            channel_link = f"https://t.me/{REQUIRED_CHANNEL[1:]}"
            
            # زر الاشتراك
            markup = telebot.types.InlineKeyboardMarkup()
            subscribe_button = telebot.types.InlineKeyboardButton(
                text="🔗 اشترك في القناة أولاً",
                url=channel_link
            )
            markup.add(subscribe_button)
            
            # رسالة الاشتراك
            bot.reply_to(
                message,
                f"⚠️ عذراً، يجب الاشتراك في القناة أولاً لاستخدام البوت!\n\n"
                f"👉 اشترك هنا: {REQUIRED_CHANNEL}\n\n"
                f"بعد الاشتراك، أرسل /start مرة أخرى.",
                reply_markup=markup
            )
            return
        return func(message)
    return wrapper

@bot.message_handler(commands=['start'])
@subscription_required
def send_welcome(message):
    bot.reply_to(
        message,
        "✅ أهلاً بك! أنا بوت ترجمة سريع ومجاني.\n"
        "📝 فقط أرسل لي أي نص وسأترجمه تلقائياً:\n"
        "• النص العربي → إنجليزي\n"
        "• النص الإنجليزي → عربي\n"
        "• أي لغة أخرى → إنجليزي"
    )

@bot.message_handler(func=lambda message: True)
@subscription_required
def translate_text(message):
    try:
        text = message.text
        
        # التحقق من النص الفارغ
        if not text or len(text.strip()) == 0:
            bot.reply_to(message, "❌ الرجاء إرسال نص للترجمة.")
            return
        
        # الكشف عن اللغة والترجمة
        if any('\u0600' <= c <= '\u06FF' for c in text):
            # إذا كان النص عربي، نترجمه للإنجليزية
            translated = GoogleTranslator(source='ar', target='en').translate(text)
            lang_info = "🇸🇦 عربي → 🇬🇧 إنجليزي"
        else:
            # إذا كان النص غير عربي، نترجمه للعربية
            translated = GoogleTranslator(source='auto', target='ar').translate(text)
            lang_info = "🌐 → 🇸🇦 عربي"
        
        # إرسال الترجمة مع معلومات اللغة
        response = f"<b>الترجمة:</b>\n{translated}\n\n<i>{lang_info}</i>"
        bot.reply_to(message, response, parse_mode='HTML')

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(
            message,
            "⚠️ عذراً، حدث خطأ أثناء الترجمة.\n"
            "تأكد من النص وحاول مرة أخرى."
        )

print("🤖 Offline Translation Bot is running...")
print(f"📢 Required channel: {REQUIRED_CHANNEL}")
print("🔄 Checking for messages...")

# تشغيل البوت
bot.polling(none_stop=True)