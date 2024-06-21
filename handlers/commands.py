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
        "Здравствуйте!!! \n"
        "Добро пожаловать в МЕДИНФОЗАПИСЬБОТ!!! \n"
        "🗺/address - Адрес \n"
        "☎/contacts - Контакты \n"
        "⌚/grafic - График работы \n"
        "📝/uslugi - Услуги \n"
        "✍/zapisatsya - Запись к врачу \n"
        "✍/add_client - Добавить клиента \n"
        "🚫/end - Завершение \n"
    )
    kb = [
        [KeyboardButton(text="/address")], [KeyboardButton(text="/contacts")],
        [KeyboardButton(text="/grafic")], [KeyboardButton(text="/uslugi")], 
        [KeyboardButton(text="/zapisatsya")],[KeyboardButton(text="/add_client")],
        [KeyboardButton(text="/end")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(description, reply_markup=keyboard)
    

# Обработчик для команды /end
@router.message(Command(commands=['end']))
async def end(message: Message):
    await message.answer("Спасибо, что воспользовались МЕДИНФОЗАПИСЬБОТОМ! До новых встреч!", show_alert=True)

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
    
        "1.Ультразвуковая диагностика \n"
        "2.Терапия \n"
        "3.Психология консультация семьи \n"
        "4.Ортопедия \n"
        "5.Лабороторная диагностика анализы \n"
        "6.Колопроктология \n"
        "7.Дерматовенералогия \n"
        "8.Акушерства и гинекология \n",
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





from aiogram.types import Message,CallbackQuery,FSInputFile,ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class AddClientStates(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    email = State()
    phone = State()
    address = State()
    department_id = State()



@router.message(Command("add_client"))
async def cmd_add_client(message:Message,state: FSMContext):
    await state.set_state(AddClientStates.first_name)
    await message.answer("Enter first name:",
    reply_markup=ReplyKeyboardRemove())
    
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )



@router.message(AddClientStates.first_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(AddClientStates.last_name)
    await message.answer("Enter last name:",
    reply_markup=ReplyKeyboardRemove())


@router.message(AddClientStates.last_name)
async def process_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(AddClientStates.age)
    await message.answer("Enter age:")


@router.message(AddClientStates.age)
async def process_salary(message: Message, state: FSMContext) -> None:
    await state.update_data(salary=float(message.text))
    await state.set_state(AddClientStates.email)
    await message.answer("Enter email:")

@router.message(AddClientStates.email)
async def process_email(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(AddClientStates.phone)
    await message.answer("Enter phone:")

@router.message(AddClientStates.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=int(message.text))
    await state.set_state(AddClientStates.address)
    await message.answer("Enter address:")

@router.message(AddClientStates.address)
async def process_address(message: Message, state: FSMContext) -> None:
    await state.update_data(address=message.text)
    await state.set_state(AddClientStates.department_id)
    await message.answer("Enter department id:")

@router.message(AddClientStates.department_id)
async def process_department_id(message: Message, state: FSMContext) -> None:
    await state.update_data(department_id=int(message.text))
    data = await state.get_data()
    await show_summary(message, data)
    await state.clear()

async def show_summary(message: Message, data: dict[str, any]):
    client = Client(first_name=data["first_name"],
              last_name=data["last_name"],
              age=data["age"],
              email=data["email"], 
              phone=data["phone"], 
              address=data["address"],
              department_id=data["department_id"])
    result = await create_client(client)
    await message.answer(text="Успешно добавили клиента", reply_markup=ReplyKeyboardRemove())
