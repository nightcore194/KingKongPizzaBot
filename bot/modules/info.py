from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot import bot

router = Router()


@router.callback_query(F.data == 'admin_info')
async def admin_info(callback: CallbackQuery) -> None:
    kb = [[InlineKeyboardButton(text="Ассортимент блюд", callback_data='food_catalog'),
           InlineKeyboardButton(text="Технологическая карта", callback_data='food_techmap')],
          [InlineKeyboardButton(text="В меню", callback_data='go_back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Выберете категорию", reply_markup=markup)


@router.callback_query(F.data.startswith("food_"))
async def food_catalog(callback: CallbackQuery) -> None:
    destination = callback.data.split("_")[1]
    if destination == "techmap":
        kb = [[InlineKeyboardButton(text='Создание рецепта', callback_data=f'create_Recipe'),
               InlineKeyboardButton(text='Посмотреть рецепты', callback_data=f'check_Recipe')]]
    else:
        kb = [[InlineKeyboardButton(text='Создание блюда', callback_data=f'create_Food'),
               InlineKeyboardButton(text='Посмотреть блюда', callback_data=f'check_Food')]]
    kb.append([InlineKeyboardButton(text="В меню", callback_data='go_back')])
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Что вы хотите сделать?", reply_markup=markup)
