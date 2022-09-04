from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# buttons at view bill
but_change = KeyboardButton('Изменить')
but_return = KeyboardButton('В начало')

kb_action_bill = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)

kb_action_bill.add(but_change, but_return)

# buttons at view bill
but_delete = KeyboardButton('Удалить еще')

kb_action_bill_del = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)

kb_action_bill_del.add(but_delete, but_return)


# buttons when choosing to view bills
def generate_bill_btn(bill_list, size_line) -> ReplyKeyboardMarkup:

    kb_bill = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_bill.row(KeyboardButton('Отмена'))

    bill_list = [KeyboardButton(x) for x in bill_list]

    while len(bill_list) != 0:
        pice = bill_list[:size_line]
        for i in pice:
            button = i
            kb_bill.row(button)
        bill_list = bill_list[size_line:]

    return kb_bill


but_bill_name = KeyboardButton('Название')
but_acc_balance = KeyboardButton('Баланс счёта')
but_is_not_calc = KeyboardButton('Учёт в общем балансе')

kb_params_bill = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)

kb_params_bill.row(but_bill_name, but_acc_balance)\
              .add(but_is_not_calc, KeyboardButton('Отмена'))


but_change_cur = KeyboardButton('Изменить этот же счёт')
but_change_oth = KeyboardButton('Изменить другой счёт')

kb_end_change_bill = ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)

kb_end_change_bill.add(but_change_cur, but_change_oth).row(but_return)
