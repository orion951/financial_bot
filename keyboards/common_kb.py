from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but_yes = KeyboardButton('Да')
but_no = KeyboardButton('Нет')

kb_close_question = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_close_question.row(but_yes, but_no)