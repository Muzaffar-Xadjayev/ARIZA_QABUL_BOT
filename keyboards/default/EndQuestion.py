from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

end = InlineKeyboardMarkup(row_width=1)
btn = InlineKeyboardButton(text="❌ Savollarim tugadi",callback_data="end_quizs")
end.add(btn)