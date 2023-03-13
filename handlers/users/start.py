import datetime

import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart
from playhouse.shortcuts import model_to_dict

from keyboards.inline.check import btn1
from data.config import ADMINS
from keyboards.inline.show_vakancy import show_vakansy
from loader import dp, db, bot
from database.models import *
from states.ariza import Ariza

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    user_name = message.from_user.username
    user_id = message.from_user.id
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    elo = Pattern.select()
    elonlar = [model_to_dict(item) for item in elo]
    btn = await show_vakansy(elonlar)
    with db:
        if not Users.select().where(Users.telegram_id == user_id).exists():
            Users.create(full_name=name,username=user_name,telegram_id=user_id,join_date=today)
            count_user = Users.select().count()
            msg1 = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count_user} ta foydalanuvchi bor."
            try:
                for user in ADMINS:
                    await bot.send_message(user, msg1,parse_mode="NONE")
            except:
                pass

    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n<b>HR Ariza Bot</b>iga xush kelibsiz!\n\n"
                             f"Siz qaysi e'longa ariza qoldirmoqchisiz👇",reply_markup=btn)

    # await Ariza.pattern.set()
@dp.message_handler(commands=['start'],state=Ariza.pattern)
async def cancel_state(message: types.Message, state:FSMContext):
    await state.finish()
    elo = Pattern.select()
    elonlar = [model_to_dict(item) for item in elo]
    btn = await show_vakansy(elonlar)
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n<b>HR Ariza Bot</b>iga xush kelibsiz!\n\n"
                             f"Siz qaysi e'longa ariza qoldirmoqchisiz👇",reply_markup=btn)
@dp.message_handler()
async def just_text(message: types.Message):
    elon = Pattern.select()
    elonlar = [model_to_dict(item) for item in elon]
    btn = await show_vakansy(elonlar)
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n<b>HR Ariza Bot</b>iga xush kelibsiz!\n\n"
                         f"Siz qaysi e'longa ariza qoldirmoqchisiz👇", reply_markup=btn)
    # await Ariza.pattern.set()

@dp.callback_query_handler(text_contains="yonalish:")
async def get_pattern(call: CallbackQuery,state:FSMContext):
    await call.message.delete()
    get_id = call.data.split("yonalish:")
    datab = Pattern.select().where(Pattern.id == int(get_id[1]))
    data_list = [model_to_dict(item) for item in datab]
    quizs = Questions.select().where(Questions.author == data_list[0]["title"])
    questions = [model_to_dict(item) for item in quizs]
    if questions:
        await call.message.answer(questions[0]["text"])
    else:
        await call.message.answer("Kechirasiz bu vakansiyaga oid savollar hali qo'shilmagan.")
    await state.update_data(
        {
            "pattern": get_id[1],
            "question": questions,
            "counter" : 0
        }
    )
    await Ariza.pattern.set()

@dp.message_handler(state=Ariza.pattern)
async def get_inf(msg: types.Message, state:FSMContext):
    user_text = msg.text
    data = await state.get_data()
    counter = data["counter"]
    question = data["question"]
    # print(question)
    key_name = question[counter]["id"]
    await state.update_data(
        {
            key_name: user_text,
            "counter":counter+1,
        }
    )
    # print(len(question),counter+1)
    if len(question)!=counter+1:
        await msg.answer(question[counter+1]["text"])
        await Ariza.pattern.set()
    else:
        data12 = await state.get_data()
        data12.pop("question")
        data12.pop("counter")
        await sort_message(data12,msg.from_user.id)
        await state.finish()
        await msg.answer("Sizni so'rovingiz qabul qilindi. Bergan javoblaringizga qarab uch ish kun ichida siz bilan bog'lanamiz. E'tiboringiz uchun rahmat ✅\n‼️ Iltimos Botdan uzoqlashmang biz siz bilan aloqaga chiqamiz.")

async def sort_message(dict,user_id):
    # name = Pattern.select().where(Pattern.id == dict["pattern"])
    vakansy_name = [model_to_dict(item) for item in Pattern.select().where(Pattern.id == dict["pattern"])]
    context=f"💼 Vakansiya: {vakansy_name[0]['title']}\n" \
            f"🆔 UserId: <code>{user_id}</code>\n"
    dict.pop("pattern")
    for i in dict.keys():
        questions = Questions.select().where(Questions.id == i)
        question_name = [model_to_dict(item) for item in questions]
        context += f"—{question_name[0]['text']}: {dict[i]}\n"
    try:
        for admin in ADMINS:
            await bot.send_message(admin, context)
    except Exception as err:
        pass

# @dp.message_handler(state=Ariza.bio)
# async def get_bio(msg: types.Message, state:FSMContext):
#     await state.update_data(
#         {"bio":msg.text}
#     )
#     await msg.answer(f"Resume ingiz bo'lsa pdf yoki document ko'rinishida junating aks holda <em>yo\'q</em> deb yozing.")
#     await Ariza.resume.set()
#
# @dp.message_handler(state=Ariza.resume, content_types=["document","file"])
# async def get_file_resume(msg: types.Message, state:FSMContext):
#     await state.update_data(
#         {"file_resume":msg.document.file_id}
#     )
#     await msg.answer("Telefon raqam yozing:\n\n"
#                      "Masalan( +998930000000 )")
#     await Ariza.tel.set()
#
# @dp.message_handler(state=Ariza.resume, content_types=["text","video","audio"])
# async def get_Text_resume(msg: types.Message, state:FSMContext):
#     await state.update_data(
#         {"text_resume":msg.text}
#     )
#     await msg.answer("Telefon raqam yozing:\n\n"
#                      "Masalan( +998930000000 )")
#     await Ariza.tel.set()
#
# @dp.message_handler(state=Ariza.tel)
# async def get_tel(msg: types.Message, state:FSMContext):
#     await state.update_data(
#         {"tel":msg.text}
#     )
#     await msg.answer("Telegram akkaunt yozing:\n"
#                      "Masalan ( @username )")
#     await Ariza.tg.set()
#
# @dp.message_handler(state=Ariza.tg)
# async def get_tg(msg: types.Message, state:FSMContext):
#     await state.update_data(
#         {"tg":msg.text}
#     )
#     data = await state.get_data()
#     try:
#         if data["file_resume"]:
#             post = f"Ma'lumotlaringizni hammasi to'g'rimi ? \n\n"
#             post += f"📝 ANKETA:\n"
#             post += f"💼 Vakansiya: {data['pattern']}\n"
#             post += f"☎️ Telefon raqam: {data['tel']}\n"
#             post += f"📎 Telegram: {data['tg']}\n"
#             post += f"👤 To'liq ma'lumot: {data['bio']}"
#             await msg.answer_document(data["file_resume"],caption=post,reply_markup=btn1)
#
#     except:
#         if data["text_resume"]:
#             post = f"Ma'lumotlaringizni hammasi to'g'rimi ? \n\n"
#             post += f"📝 ANKETA:\n"
#             post += f"💼 Vakansiya: {data['pattern']}\n"
#             post += f"☎️ Telefon raqam: {data['tel']}\n"
#             post += f"📎 Telegram: {data['tg']}\n"
#             post += f"👤 To'liq ma'lumot: {data['bio']}"
#             await msg.answer(post,reply_markup=btn1)
#     await Ariza.check.set()
#
# @dp.callback_query_handler(state=Ariza.check,text="xa")
# async def check(call: CallbackQuery,state:FSMContext):
#     await call.answer(cache_time=60)
#     await call.message.delete()
#     await call.message.answer(f"Sizni so'rovingiz qabul qilindi. Bergan javoblaringizga qarab uch ish kun ichida siz bilan bo'g'lanishadi. Agar bog'lanilmasa  demak siz qabul qilinmagansiz. E'tiboringiz uchun rahmat ✅")
#     data = await state.get_data()
#     try:
#         if data["file_resume"]:
#             post = f"📝 ANKETA:\n"
#             post += f"🆔 UserID: <code>{call.from_user.id}</code>\n"
#             post += f"💼 Vakansiya: {data['pattern']}\n"
#             post += f"☎️ Telefon raqam: {data['tel']}\n"
#             post += f"📎 Telegram: {data['tg']}\n"
#             post += f"👤 To'liq ma'lumot: {data['bio']}"
#             try:
#                 for i in ADMINS:
#                     await bot.send_document(chat_id=i, document=data["file_resume"], caption=post)
#             except:
#                 pass
#     except:
#         if data["text_resume"]:
#             post = f"📝 ANKETA:\n"
#             post += f"🆔 UserID: <code>{call.from_user.id}</code>\n"
#             post += f"💼 Vakansiya: {data['pattern']}\n"
#             post += f"☎️ Telefon raqam: {data['tel']}\n"
#             post += f"📎 Telegram: {data['tg']}\n"
#             post += f"👤 To'liq ma'lumot: {data['bio']}"
#             try:
#                 for i in ADMINS:
#                     await bot.send_message(chat_id=i, text=post)
#             except:
#                 pass
#     await state.finish()
#
# @dp.callback_query_handler(text="yoq",state=Ariza.check)
# async def cancel_a(call: CallbackQuery, state:FSMContext):
#     await call.answer(cache_time=60)
#     await call.message.delete()
#     await call.message.answer(f"Assalomu alaykum hurmatli {call.from_user.full_name}, ariza yuborish bekor qilindi. Qaytadan ariza to'ldiring.\n\n")
#     await state.finish()