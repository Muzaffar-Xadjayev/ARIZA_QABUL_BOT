from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('📲 Telefon raqam yuborish',request_contact=True),
        ],
    ],
    resize_keyboard=True
)

otmen = InlineKeyboardMarkup(row_width=1)
btn = InlineKeyboardButton("🔙 Bekor qilish",callback_data="cc")
otmen.add(btn)