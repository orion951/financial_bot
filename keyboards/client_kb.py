from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but_expenses = KeyboardButton('Расходы')
but_income = KeyboardButton('Доходы')
but_bills = KeyboardButton('Счета')
but_kategories = KeyboardButton('Категории')
but_report = KeyboardButton('Отчет')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(but_expenses, but_income).row(but_bills, but_kategories, but_report)