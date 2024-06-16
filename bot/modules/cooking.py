from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot import bot

router = Router()


@router.callback_query(F.data == 'cook_order')
async def admin_info(callback: CallbackQuery) -> None:
    kb = [[InlineKeyboardButton(text="Посмотреть заказы", callback_data='check_Order'),
           InlineKeyboardButton(text="Технологическая карта", callback_data='food_techmap')],
          [InlineKeyboardButton(text="В меню", callback_data='go_back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Что вы хотите сделать?", reply_markup=markup)

