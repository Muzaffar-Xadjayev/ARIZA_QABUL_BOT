from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp
from states.ariza import Ariza
from loader import dp


@dp.message_handler(CommandHelp())
async def help_user(message: types.Message):
    msg = f"Bot Tomonidan foydalanuvchiga yordam ko'rsatish bo'limi\n" \
          f"Buyruqlar:\n/start — Botni ishga tushirish\n" \
          f"/help — Yordam Ko'rsatish va Bot ishlash tartibi\n\n" \
          f"<b>Botni ishlash tartibi</b>\n\n" \
          f"1.Bu bot orqali siz kanallarda berilgan e'lonlarimizga ariza qoldirishingiz mumkin." \



    await message.reply(msg)

@dp.message_handler(commands=["help"],state=Ariza.pattern)
async def cancel_help(msg: types.Message,state:FSMContext):
    await state.finish()
    msg1 = f"Bot Tomonidan foydalanuvchiga yordam ko'rsatish bo'limi\n" \
          f"Buyruqlar:\n/start — Botni ishga tushirish\n" \
          f"/help — Yordam Ko'rsatish va Bot ishlash tartibi\n\n" \
          f"<b>Botni ishlash tartibi</b>\n\n" \
          f"1.Bu bot orqali siz kanallarda berilgan e'lonlarimizga ariza qoldirishingiz mumkin."
    await msg.answer(msg1)

