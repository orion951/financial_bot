from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but_expenses = KeyboardButton('Расходы')
but_income = KeyboardButton('Доходы')
but_bills = KeyboardButton('Счета')
but_kategories = KeyboardButton('Категории')
but_report = KeyboardButton('Отчет')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(but_expenses, but_income).row(but_bills, but_kategories, but_report)

but_create = KeyboardButton('Создать')
but_change = KeyboardButton('Изменить')
but_delete = KeyboardButton('Удалить')
but_show = KeyboardButton('Посмотреть')

kb_action = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_action.row(but_create, but_change).row(but_delete, but_show)