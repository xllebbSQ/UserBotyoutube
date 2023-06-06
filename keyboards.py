from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def video():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    send = KeyboardButton(text="Отправить видео")
    keyboard.add(send)
    return keyboard