import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from models import db, Order
from sqlalchemy import func
from bot.bot import bot
from bot.states import StatesReport

router = Router()


@router.callback_query(F.data == 'admin_report')
async def admin_info(callback: CallbackQuery) -> None:
    kb = [[InlineKeyboardButton(text="Анализ продаж за весь период", callback_data='analyze_all'),
           InlineKeyboardButton(text="Анализ продаж за конкретный период", callback_data='analyze_period')],
          [InlineKeyboardButton(text="В меню", callback_data='go_back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Что вы хотите сделать?", reply_markup=markup)


@router.callback_query(F.data.startswith("analyze_"))
async def analyze(callback: CallbackQuery, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data='go_back')]])
    analyze_type = callback.data.split('_')[1]
    match analyze_type:
        case "all":
            result = db.query(func.sum(Order.price).label("sum_price")).first()
            if result.sum_price is not None:
                price = float(result.sum_price)
            else:
                price = 0
            await bot.send_message(callback.from_user.id,
                                   f"Сумма продаж за весь период - {price}", reply_markup=markup)
        case "period":
            await state.set_state(StatesReport.inputEndDate)
            await bot.send_message(callback.from_user.id, "Введите начальную дату в формате дд.мм.гггг")


@router.message(StatesReport.inputEndDate, F.text.regexp(r'\d{2}.\d{2}.\d{4}'))
async def analyze_input_date(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите конечную дату", reply_markup=markup)
    await state.set_state(StatesReport.result)
    await state.set_data(dict(start_date=message.text))


@router.message(StatesReport.result, F.text.regexp(r'\d{2}.\d{2}.\d{4}'))
async def analyze_date(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    start_date = datetime.strptime(data["start_date"], "%d.%m.%Y").strftime("%Y-%m-%d")
    logging.debug(start_date)
    end_date = datetime.strptime(message.text, "%d.%m.%Y").strftime("%Y-%m-%d")
    logging.debug(end_date)
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data='go_back')]])
    result = db.query(func.sum(Order.price).label("sum_price")).filter(Order.date.between(start_date, end_date)).first()
    logging.debug(result)
    if result.sum_price is not None:
        price = float(result.sum_price)
    else:
        price = 0
    await state.clear()
    await bot.send_message(message.from_user.id,
                           f"Сумма продаж за период c {data["start_date"]} по {message.text} - {price}",
                           reply_markup=markup)


@router.message(StatesReport.result)
async def analyze_input_result_error(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Неверно введена дата", reply_markup=markup)


@router.message(StatesReport.inputEndDate)
async def analyze_input_date_error(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Неверно введена дата", reply_markup=markup)

