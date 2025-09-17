import os
import telebot
from telebot import types
from flask import Flask
import threading

API_TOKEN = os.environ.get('API_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

bot = telebot.TeleBot(API_TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot aktif ✅"

def keep_alive():
    app.run(host='0.0.0.0', port=8080)

buton_cevaplari = {
    "odeme": {
        "buton": "💳 Ödeme Yöntemleri",
        "yanit": "Mobilonay.net'te Kredi Kartı, Papara ve Kripto ile ödeme yapabilirsiniz."
    },
    "fiyat": {
        "buton": "📊 Fiyatlar",
        "yanit": "Güncel fiyatlarımız için: https://mobilonay.net/servis"
    },
    "iptal": {
        "buton": "❌ Sipariş İptali",
        "yanit": "Sipariş iptali için hesabınıza giriş yapın ve 'İptal Et' butonuna tıklayın."
    },
    "hesap": {
        "buton": "📝 Hesap Oluşturma",
        "yanit": "Yeni hesap oluşturmak için: https://mobilonay.net/kayit-ol → 'Kayıt Ol'"
    }
}

@bot.message_handler(commands=['start'])
def basla(message):
    markup = types.InlineKeyboardMarkup()
    for key, data in buton_cevaplari.items():
        markup.add(types.InlineKeyboardButton(data["buton"], callback_data=key))
    markup.add(types.InlineKeyboardButton("👤 Müşteri Temsilcisine Bağlan", url='https://t.me/mobilonaynet'))

    mesaj = (
        "Merhaba 👋\n"
        "Mobilonay.net destek botuna hoş geldin.\n\n"
        "Aşağıdan bir konu seç:"
    )
    bot.send_message(message.chat.id, mesaj, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def buton_cevapla(call):
    key = call.data
    user = call.from_user
    if key in buton_cevaplari:
        yanit = buton_cevaplari[key]["yanit"]
        bot.send_message(call.message.chat.id, yanit)

        # Admin bildirimi
        if ADMIN_ID:
            bildirim = (
                f"📩 Kullanıcı: @{user.username or user.first_name}\n"
                f"🆔 ID: {user.id}\n"
                f"🔘 Buton: {buton_cevaplari[key]['buton']}"
            )
            bot.send_message(ADMIN_ID, bildirim)

# Start web server ve bot
if __name__ == "__main__":
    threading.Thread(target=keep_alive).start()
    bot.polling()
