from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def show_vakansy(elonlar):
    vakancy = InlineKeyboardMarkup(row_width=3)
    vakancy.add(*[InlineKeyboardButton(text=i["title"],callback_data=f"yonalish:{i['id']}") for i in elonlar])
    return vakancy

async def show_vakansy1(elonlar):
    vakancy = InlineKeyboardMarkup(row_width=3)
    vakancy.add(*[InlineKeyboardButton(text=i["title"], callback_data=f"yonalish:{i['id']}") for i in elonlar])
    btn1 = InlineKeyboardButton(text="🔙 Bekor qilish",callback_data="cancel")
    vakancy.add(btn1)
    return vakancy

