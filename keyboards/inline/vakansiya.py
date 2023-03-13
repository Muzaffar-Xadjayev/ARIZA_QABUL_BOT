from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

manage = InlineKeyboardMarkup(row_width=2)
plus = InlineKeyboardButton(text="➕ Vakansiya Qo'shish", callback_data="plus")
minus = InlineKeyboardButton(text="➖ Vakansiya O'chirish", callback_data="minus")
question = InlineKeyboardButton(text="⬆️ Savol Qo'shish", callback_data="inc_question")
question_minus = InlineKeyboardButton(text="❌ Savol O'chirish", callback_data="dec_question")
manage.add(plus,minus,question,question_minus)