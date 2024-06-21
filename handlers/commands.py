from aiogram import Router, F
from aiogram.filters import Command, CommandStart 
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
)

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    description = (
        "Здравствуйте \n"
        "Добро пожаловать в инфозаписьбот \n"
        "/address - Адрес \n"
        "/contacts - Контакты \n"
        "/grafic - График работы \n"
        "/uslugi - Услуги \n"
        "/zapisatsya - Запись к врачу \n"
        "/end - Завершение \n"
    )
    kb = [
        [KeyboardButton(text="/address")], [KeyboardButton(text="/contacts")],
        [KeyboardButton(text="/grafic")], [KeyboardButton(text="/uslugi")], 
        [KeyboardButton(text="/zapisatsya")],[KeyboardButton(text="/end")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(description, reply_markup=keyboard)
    

# Обработчик для команды /end
@router.message(Command(commands=['end']))
async def end(message: Message):
    await message.answer("Спасибо, что воспользовались инфозаписьботом! До новых встреч!", show_alert=True)

@router.message(Command(commands=['address']))
async def address(message:Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]  # Кнопка назад
    ])
    await message.answer(
        "Адрес  \n"
        "Улица Юлиуса Фучика, 15, Ленинский район, Бишкек, 720054 \n"
        "Ссылка, на Центр семейной медицины №1  -  https://2gis.kg/bishkek/firm/70000001079855081 \n",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.delete()  # Удаляем текущее сообщение
    await start(callback.message)


@router.message(Command(commands=['contacts']))
async def contacts(message:Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]  # Кнопка назад
    ])
    await message.answer(
        "Контакты \n"
        "Тел: \n"
        "взрослая регистратура (+996 (312) 64-45-42) \n"
        "детская регистратура (+996 (312) 64-45-40) \n"
        "whatsApp: wa.me// 0(550) 104 301 \n"
        "Instagram: https://www.instagram.com/csm.1gov.kg/ \n",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.delete()  # Удаляем текущее сообщение
    await start(callback.message)


@router.message(Command(commands=['grafic']))
async def grafic(message:Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]  # Кнопка назад
    ])
    await message.answer(
        "График работы \n"
        "Понедельник - Суббота с 08:00 - 18:00 \n"
        "Выходной - Воскресенье \n",
        reply_markup=keyboard
        )

@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.delete()  # Удаляем текущее сообщение
    await start(callback.message)




@router.message(Command(commands=['uslugi']))
async def uslugi(message:Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]  # Кнопка назад
    ])
    await message.answer(
    
        "1.УЛЬТРАЗВУКОВАЯ ДИАГНОСТИКА \n"
        "2.ТЕРАПИЯ \n"
        "3.ПСИХОЛОГИЯ КОНСУЛЬТАЦИЯ СЕМЬИ \n"
        "4.ОРТОПЕДИЯ \n"
        "5.ЛАБОРАТОРНАЯ ДИАГНОСТИКА АНАЛИЗЫ \n"
        "6.КОЛОПРОКТОЛОГИЯ \n"
        "7.ДЕРМАТОВЕНЕРОЛОГИЯ \n"
        "8.АКУШЕРСТВО И ГИНЕКОЛОГИЯ \n",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.delete()  # Удаляем текущее сообщение
    await start(callback.message)




from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from main import *


ADMIN_CHAT_ID = ("5648090698")  # вставляете свой chat id
bot_instance: Bot = None  # Глобальная переменная для хранения экземпляра бота


class Form(StatesGroup):
    name = State()  # Состояние для ФИО
    phone_number = State()  # Состояние для номера телефона


def setup_routers(dispatcher: Dispatcher, bot: Bot):
    global bot_instance
    bot_instance = bot  # Сохраняем экземпляр бота для использования в хэндлерах
    dispatcher.include_router(router)


@router.message(Command("zapisatsya"))
async def cmd_zapisatsya(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваше ФИО:")
    await state.set_state(Form.name)

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Спасибо! Теперь введите ваш номер телефона:")
    await state.set_state(Form.phone_number)


@router.message(Form.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()

    # Отправляем сообщение пользователю
    await message.answer(
        f"Записаны! \nФИО: {data['name']}\nНомер телефона: {data['phone_number']}"
    )
    
    # Отправляем сообщение администратору
    user = message.from_user
    admin_message = (
        f"Новый клиент! Позвоните для потверждения записи! \n"
        f"ФИО: {data['name']}\n"
        f"Номер телефона: {data['phone_number']}"
    )
    # await message.answer(ADMIN_CHAT_ID, admin_message)
    await bot_instance.send_message(ADMIN_CHAT_ID, admin_message)

    await state.clear()