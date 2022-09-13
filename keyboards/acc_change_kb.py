from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# buttons when changing the balance
btn_expense = KeyboardButton('Расход')
btn_income = KeyboardButton('Доход')

kb_acc_change = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)

kb_acc_change.add(btn_expense, btn_income)

# buttons at end of create changing the balance
but_return = KeyboardButton('В начало')

kb_end_acc_change = ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)

kb_end_acc_change.add(btn_expense, btn_income).row(but_return)