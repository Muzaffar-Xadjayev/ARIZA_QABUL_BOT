from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admins_command = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('📝 Xabar Yuborish'),
        ],
        [
            KeyboardButton('👤 Foydalanuvchilar'),
            KeyboardButton('👮🏼‍♂️ Adminlar'),
        ],
        [
            KeyboardButton('💼 Vakansiyalar')
        ],
        [
            KeyboardButton('🔙 Chiqish')
        ]

    ],
    resize_keyboard=True
)