import telebot
from sheets import save_to_sheets

BOT_TOKEN = "Token"

bot = telebot.TeleBot(BOT_TOKEN)

# простое хранилище состояний
users = {}  # user_id -> {"step": "name/phone/comment", "name":..., ...}

@bot.message_handler(commands=["start"])
def start(message):
    users[message.chat.id] = {"step": "name"}
    bot.send_message(message.chat.id, "Привет! Введите ваше имя:")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    user_id = message.chat.id

    if user_id not in users:
        bot.send_message(user_id, "Напишите /start чтобы начать.")
        return

    step = users[user_id]["step"]

    if step == "name":
        users[user_id]["name"] = message.text.strip()
        users[user_id]["step"] = "phone"
        bot.send_message(user_id, "Введите номер телефона:")
        return

    if step == "phone":
        users[user_id]["phone"] = message.text.strip()
        users[user_id]["step"] = "comment"
        bot.send_message(user_id, "Введите комментарий:")
        return

    if step == "comment":
        users[user_id]["comment"] = message.text.strip()

        name = users[user_id]["name"]
        phone = users[user_id]["phone"]
        comment = users[user_id]["comment"]

        # запись в Google Sheets
        try:
            save_to_sheets(name, phone, comment)
            bot.send_message(user_id, "✅ Заявка принята и сохранена в таблицу!")
        except Exception as e:
            bot.send_message(user_id, f"❌ Ошибка записи в таблицу: {e}")

        # очистка состояния
        users.pop(user_id, None)
        return

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
