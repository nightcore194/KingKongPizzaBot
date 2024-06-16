import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ErrorEvent, ReplyKeyboardRemove, WebAppInfo, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from bot.states import States
from models import db, Employee, Order
from bot.text import *  # this is necessary to change replices of web, but not in the botview code
from settings.settings import *
from bot.validation import isAdmin

config = json.load(open(CONFIG_FILE))

""" INITING BOT """

bot = Bot(token=config["bot_token"])
dp = Dispatcher(bot=bot)

""" STARTUP ON WEBHOOK """


async def on_startup() -> None:
    await bot.set_webhook(BOT_WEBHOOK)


""" EXEPTION HANDLER """


@dp.error()
async def error_handler(event: ErrorEvent, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    db.rollback()
    await state.clear()
    await bot.send_message(chat_id=event.update.message.from_user.id, text="Произошла ошибка!",
                           reply_markup=markup)


""" BASIC FUNCTIONALITY """


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext) -> None:
    if db.query(Employee).filter(Employee.telegram_id == message.from_user.id).first():
        await bot.send_message(message.from_user.id, "Привет! Для того что бы авторизоваться,"
                                                     " введите свой номер телефона")
        await state.set_state(States.register)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data="go_back")]])
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup=markup)


""" APPEND TELEGRAM ID TO EXITING EMPLOYEE """


@dp.message(States.register)
async def completeRegister(message: Message) -> None:
    obj = db.query(Employee).filter(Employee.phone == message.text).first()
    if obj:
        obj.telegram_id = message.from_user.id
        db.add(obj)
        db.commit()
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data="go_back")]])
        await bot.send_message(message.from_user.id, "Вы успешно зарегистрировались!", reply_markup=markup)
    else:
        await bot.send_message(message.from_user.id, "Введите корректный номер телефона.")


""" MENU """


@dp.message(Command("menu"))
async def menu(message: Message) -> None:
    kb = []
    if isAdmin(message.from_user.id):
        kb.append([InlineKeyboardButton(text=MENU_ADMIN_ORDER, callback_data='admin_order'),
                   InlineKeyboardButton(text=MENU_ADMIN_INFO, callback_data='admin_info'),
                   InlineKeyboardButton(text=MENU_ADMIN_REPORT, callback_data='admin_report')])
        markup = InlineKeyboardMarkup(inline_keyboard=kb)
    else:
        kb.append([InlineKeyboardButton(text=MENU_ADMIN_ORDER, callback_data='cook_order'),
                   InlineKeyboardButton(text=MENU_ADMIN_INFO, callback_data='cook_techmap')])
        markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(message.from_user.id, "Что вы хотите сделать?", reply_markup=markup)


""" HANDLE GO BACK BUTTON IN INLINE KB """


@dp.callback_query(F.data == 'go_back')
async def goBack(call: CallbackQuery, state: FSMContext) -> None:
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.clear()
    kb = []
    if isAdmin(call.from_user.id):
        kb.append([InlineKeyboardButton(text=MENU_ADMIN_ORDER, callback_data='admin_order'),
                   InlineKeyboardButton(text=MENU_ADMIN_INFO, callback_data='admin_info'),
                   InlineKeyboardButton(text=MENU_ADMIN_REPORT, callback_data='admin_report')])
        markup = InlineKeyboardMarkup(inline_keyboard=kb)
    else:
        kb.append([InlineKeyboardButton(text=MENU_ADMIN_ORDER, callback_data='cook_order'),
                   InlineKeyboardButton(text=MENU_ADMIN_INFO, callback_data='check_Recipe')])
        markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(call.from_user.id, "Что вы хотите сделать?", reply_markup=markup)



