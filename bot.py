import telebot
import random

TOKEN = "6476090487:AAGqTK1v_jnZP04cSK1ifwTXf-_A5PoBaqo"  # Твой токен

bot = telebot.TeleBot(TOKEN)

facts = {
    "География": [
        "1. Самая длинная река — Нил.",
        "2. Самая глубокая точка — Марианская впадина.",
        "3. Самая высокая гора — Эверест.",
    ],
    "Физика": [
        "1. Свет — электромагнитная волна.",
        "2. Звук не распространяется в вакууме.",
        "3. Масса и вес — разные понятия.",
    ],
    "Геометрия": [
        "1. Сумма углов треугольника — 180°.",
        "2. У квадрата все стороны равны и углы прямые.",
        "3. Диагонали ромба пересекаются под углом 90°.",
    ]
}

subjects = list(facts.keys())

def create_keyboard():
    from telebot.types import ReplyKeyboardMarkup, KeyboardButton
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[KeyboardButton(subj) for subj in subjects])
    keyboard.add(KeyboardButton("Еще факт"), KeyboardButton("Выбрать предмет"))
    return keyboard

current_subject = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Напиши название предмета, чтобы получить факт.\nДоступные предметы: " + ", ".join(subjects),
                     reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text in subjects)
def send_fact(message):
    subject = message.text
    current_subject[message.chat.id] = subject
    fact = random.choice(facts[subject])
    bot.send_message(message.chat.id, f"{subject} — факт:\n{fact}", reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == "Еще факт")
def send_another_fact(message):
    subject = current_subject.get(message.chat.id)
    if not subject:
        bot.send_message(message.chat.id, "Сначала выбери предмет.", reply_markup=create_keyboard())
    else:
        fact = random.choice(facts[subject])
        bot.send_message(message.chat.id, f"{subject} — факт:\n{fact}", reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == "Выбрать предмет")
def choose_subject(message):
    bot.send_message(message.chat.id, "Выбери предмет:", reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: True)
def default_handler(message):
    bot.send_message(message.chat.id, "Пожалуйста, выбери предмет из меню или нажми /start.", reply_markup=create_keyboard())

if __name__ == "__main__":
    print("Bot started")
    bot.infinity_polling()
