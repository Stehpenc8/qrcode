from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='генерация qr кода по тексту')],
                                     [KeyboardButton(text='генерация qr кода по изображению')]],
                                     resize_keyboard=True)