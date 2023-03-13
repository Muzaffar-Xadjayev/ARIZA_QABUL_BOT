from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
btn1 = InlineKeyboardMarkup(row_width=2)
yes = InlineKeyboardButton(text="Xa",callback_data="xa")
no = InlineKeyboardButton(text="Yo'q",callback_data="yoq")
btn1.add(yes,no)