from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🔙 Bekor qilish',callback_data="bekor_qilish")
        ]
    ]
)

ads = InlineKeyboardMarkup(row_width=2)
btn = InlineKeyboardButton(text="👥 Xammaga",callback_data="hammaga")
btn1 = InlineKeyboardButton(text="👤 Bir kishiga",callback_data="bir_kishi")
ads.add(btn,btn1)
