import datetime

from aiogram.types import Message,CallbackQuery
from aiogram.dispatcher import FSMContext
from playhouse.shortcuts import model_to_dict
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.ads import admins_command
from keyboards.inline.choose_format import cancel
from states.ads import Delete,Create,Add_Question,Remove_Question
from keyboards.inline.show_vakancy import show_vakansy, show_vakansy1
from keyboards.default.EndQuestion import end
from keyboards.inline.vakansiya import manage
from data.config import ADMINS
from loader import dp,db,bot
from database.models import *

try:
    @dp.message_handler(text="💼 Vakansiyalar",user_id=ADMINS)
    async def show_all_vakansy(msg: Message):
        a = Pattern.select()
        all_vakansy = [model_to_dict(item) for item in a]
        text = "Botdagi barcha vakansiyalar:\n\n"
        a = 0
        for i in all_vakansy:
            a += 1
            text += f"{a}. {i['title']}\n"
        await msg.answer(text,reply_markup=manage)

    @dp.callback_query_handler(text="dec_question")
    async def dec_quiz(call: CallbackQuery):
        await call.message.delete()
        await call.answer(cache_time=60)
        with db:
            elo = Pattern.select()
            elonlar = [model_to_dict(item) for item in elo]
            btn = await show_vakansy1(elonlar)
        text = f"Qaysi Vakansiyani savolini o'chirmoqchisiz ?"
        await call.message.answer(text, reply_markup=btn)
        await Remove_Question.title.set()


    @dp.callback_query_handler(text="cancel", state=Remove_Question.title)
    async def home2(call: CallbackQuery, state: FSMContext):
        await call.message.delete()
        await call.message.answer("Savol o'chirish bekor qilindi.")
        await call.answer(cache_time=60)
        vakansy = Pattern.select()
        all_vakansy = [model_to_dict(item) for item in vakansy]
        text = "Botdagi barcha vakansiyalar:\n\n"
        a = 0
        for i in all_vakansy:
            a += 1
            text += f"{a}. {i['title']}\n"
        await call.message.answer(text, reply_markup=manage)
        await state.finish()

    @dp.callback_query_handler(state=Remove_Question.title)
    async def dec_q(call: CallbackQuery, state:FSMContext):
        await call.answer(cache_time=60)
        await call.message.delete()
        splited_id = call.data.split("yonalish:")
        title = [model_to_dict(item) for item in Pattern.select().where(Pattern.id == splited_id[1])]
        with db:
            Questions.delete().where(Questions.author_id == title[0]["title"]).execute()
        await call.message.answer(f"{title[0]['title']} ga tegishli savollarni barchasi o'chirildi.")
        await state.finish()



    @dp.callback_query_handler(text="inc_question")
    async def inc_ques(call: CallbackQuery):
        await call.message.delete()
        await call.answer(cache_time=60)
        with db:
            elo = Pattern.select()
            elonlar = [model_to_dict(item) for item in elo]
            btn = await show_vakansy1(elonlar)
        text = f"Qaysi Vakansiyaga savol qo'shmoqchisiz ?"
        await call.message.answer(text,reply_markup=btn)
        await Add_Question.title.set()


    @dp.callback_query_handler(text="cancel", state=Add_Question.title)
    async def home2(call: CallbackQuery, state: FSMContext):
        await call.answer(cache_time=60)
        await call.message.delete()
        vakansy = Pattern.select()
        all_vakansy = [model_to_dict(item) for item in vakansy]
        text = "Botdagi barcha vakansiyalar:\n\n"
        a = 0
        for i in all_vakansy:
            a += 1
            text += f"{a}. {i['title']}\n"
        await call.message.answer(text, reply_markup=manage)
        await state.finish()

    @dp.callback_query_handler(state=Add_Question.title)
    async def get_additional_title(call: CallbackQuery, state:FSMContext):
        await state.update_data(
            {"title":call.data}
        )
        splited_id = call.data.split("yonalish:")
        title = [model_to_dict(item) for item in Pattern.select().where(Pattern.id == splited_id[1])]
        await call.message.edit_text(f"{title[0]['title']} ga oid 1-savolingizni yozing: ")
        await Add_Question.text.set()

    @dp.callback_query_handler(text="end_quizs", state=Add_Question.text)
    async def end_question(call: CallbackQuery, state:FSMContext):
        await call.message.delete()
        await state.finish()
        await call.message.answer("Savollar muvaffaqiyatli qo'shildi.",reply_markup=admins_command)
        a = Pattern.select()
        all_vakansy = [model_to_dict(item) for item in a]
        text = "Botdagi barcha vakansiyalar:\n\n"
        a = 0
        for i in all_vakansy:
            a += 1
            text += f"{a}. {i['title']}\n"
        await call.message.answer(text, reply_markup=manage)

    @dp.message_handler(state=Add_Question.text)
    async def question_text(msg: Message,state:FSMContext):
        data = await state.get_data()
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        splited_id = data['title'].split("yonalish:")
        title = [model_to_dict(item) for item in Pattern.select().where(Pattern.id == splited_id[1])]
        with db:
            Questions.create(author=title[0]["title"],text=msg.text,join_date=today)
        await msg.answer("Keyingi savolni kiriting:\n"
                         "( Agar savollaringiz tugagan bo'lsa \"❌ Savollarim tugadi\" tugmasini bosing. )",reply_markup=end)
        await Add_Question.text.set()




    @dp.callback_query_handler(text="minus")
    async def click_btn(call: CallbackQuery):
        await call.answer(cache_time=60)
        elon = Pattern.select()
        elonlar = [model_to_dict(item) for item in elon]
        btn = await show_vakansy1(elonlar)
        await call.message.edit_text("Qaysi vakansiyani o'chirmoqchisiz",reply_markup=btn)
        await Delete.msg.set()


    @dp.callback_query_handler(text="plus")
    async def add_vak(call: CallbackQuery):
        await call.answer(cache_time=60)
        await call.message.edit_text("Yangi vakansiyaning nomini kiriting:\n\n"
                                     "Masalan ( Frontend ) ",reply_markup=cancel)
        await Create.title.set()

    @dp.message_handler(state=Create.title,user_id=ADMINS)
    async def get_title(msg: Message, state:FSMContext):
        await state.update_data(
            {"title":msg.text}
        )
        await Create.question.set()
        data = await state.get_data()
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with db:
            if not Pattern.select().where(Pattern.title == data["title"]).exists():
                Pattern.create(title=data["title"],join_date=today)
                await msg.answer("Yangi vakansiya muvaffaqiyatli qo'shildi.")
                all = Pattern.select()
                all_vakansy = [model_to_dict(item) for item in all]
                text = "Botdagi barcha vakansiyalar:\n\n"
                a = 0
                for i in all_vakansy:
                    a += 1
                    text += f"{a}. {i['title']}\n"
                await msg.answer(text, reply_markup=manage)
            else:
                await msg.answer("Bu Vakansiya avval yaratilgan.")
        await state.finish()

    @dp.callback_query_handler(text="bekor_qilish", state=Create.title)
    async def home(call: CallbackQuery, state: FSMContext):
        await call.answer(cache_time=60)
        await call.message.delete()
        avakansy = Pattern.select()
        all_vakansy = [model_to_dict(item) for item in avakansy]
        text = "Botdagi barcha vakansiyalar:\n\n"
        a = 0
        for i in all_vakansy:
            a += 1
            text += f"{a}. {i['title']}\n"
        await call.message.answer(text, reply_markup=manage)
        await state.finish()

    @dp.callback_query_handler(text="cancel", state=Delete.msg)
    async def home2(call: CallbackQuery, state: FSMContext):
        await call.answer(cache_time=60)
        await call.message.delete()
        vakansy = Pattern.select()
        all_vakansy = [model_to_dict(item) for item in vakansy]
        text = "Botdagi barcha vakansiyalar:\n\n"
        a = 0
        for i in all_vakansy:
            a += 1
            text += f"{a}. {i['title']}\n"
        await call.message.answer(text, reply_markup=manage)
        await state.finish()





    @dp.callback_query_handler(state=Delete.msg)
    async def delete(call: CallbackQuery, state: FSMContext):
        await call.answer(cache_time=60)
        await call.message.delete()
        splited_id = call.data.split("yonalish:")
        title = [model_to_dict(item) for item in Pattern.select().where(Pattern.id == splited_id[1])]
        with db:
            Pattern.delete().where(Pattern.title == title[0]["title"]).execute()
        await call.message.answer("O'chirildi")

        vakansy = Pattern.select()
        all_vakansy = [model_to_dict(item) for item in vakansy]
        text = "Botdagi barcha vakansiyalar:\n\n"
        a = 0
        for i in all_vakansy:
            a += 1
            text += f"{a}. {i['title']}\n"
        await call.message.answer(text, reply_markup=manage)
        await state.finish()



except:
    pass
