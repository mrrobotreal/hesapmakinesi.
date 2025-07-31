from flask import Flask, request
import telegram
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def calculate(expression):
    try:
        allowed = "0123456789+-*/.() "
        if any(char not in allowed for char in expression):
            return "❌ Geçersiz karakter!"
        result = eval(expression)
        return f"🧮 Sonuç: {result}"
    except ZeroDivisionError:
        return "❌ Sıfıra bölme hatası!"
    except Exception:
        return "❌ Geçersiz ifade!"

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    user_message = update.message.text.strip()
    answer = calculate(user_message)
    bot.send_message(chat_id=chat_id, text=answer)
    return 'ok'

@app.route('/')
def index():
    return "Bot çalışıyor."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))