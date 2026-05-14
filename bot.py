import telebot
import yt_dlp
import os

TOKEN = "8335947303:AAFgLpm9AwNkPr2LVu3pwWKx5ShATzBd1vw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ഹലോ സോനു! വീഡിയോ ലിങ്ക് അയക്കൂ...")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "instagram.com" in url:
        msg = bot.reply_to(message, "ഡൗൺലോഡ് ചെയ്യുന്നു... ⏳")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            if os.path.exists(filename):
                os.remove(filename)
            bot.delete_message(message.chat.id, msg.message_id) 
            
        except Exception as e:
            bot.edit_message_text("ക്ഷമിക്കണം, ഈ വീഡിയോ ഡൗൺലോഡ് ചെയ്യാൻ കഴിഞ്ഞില്ല.", chat_id=message.chat.id, message_id=msg.message_id)
    else:
        bot.reply_to(message, "ശരിയായ ലിങ്ക് അയക്കൂ.")

bot.infinity_polling()
