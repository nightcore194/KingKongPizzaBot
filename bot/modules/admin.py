from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from sqlalchemy import desc
from bot.states import StatesAdmin, StatesInfo
from bot.validation import isAdmin
from models import *
from bot.bot import bot

router = Router()


@router.callback_query(F.data == 'admin_order')
async def admin_order(callback: CallbackQuery) -> None:
    kb = [[InlineKeyboardButton(text="Самовывоз", callback_data='order_dropoff'),
           InlineKeyboardButton(text="Доставка", callback_data='order_delivery')],
          [InlineKeyboardButton(text="Клиент", callback_data='admin_order_client'),
           InlineKeyboardButton(text="В меню", callback_data='go_back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Выберете категорию", reply_markup=markup)


@router.callback_query(F.data.startswith("admin_order_client"))
async def client_menu(callback: CallbackQuery) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить нового клиента", callback_data='add_Client'),
         InlineKeyboardButton(text="Посмотреть клиентов", callback_data='check_Сlient')],
        [InlineKeyboardButton(text='В меню', callback_data='go_back')]
    ])
    await bot.send_message(callback.from_user.id, "Что вы хотите сделать?", reply_markup=markup)


@router.callback_query(F.data.startswith("order_"))
async def order_info(callback: CallbackQuery) -> None:
    order_type = callback.data.split('_')[1]
    kb = [[InlineKeyboardButton(text='Создание заказа', callback_data=f'add_Order_{order_type}'),
           InlineKeyboardButton(text='Посмотреть заказы', callback_data=f'check_Order_{order_type}')],
          [InlineKeyboardButton(text="В меню", callback_data='go_back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Что вы хотите сделать?", reply_markup=markup)


""" CREATION LOGIC STEP BY STEP"""


@router.callback_query(F.data.startswith("add_"))
async def create_order(callback: CallbackQuery, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    class_name = callback.data.split('_')[1]
    text = "Введите имя "
    await state.set_data(dict(class_name=class_name))
    match class_name:
        case "Order":
            await state.set_state(StatesAdmin.inputFood)
            text += "заказа"
            await state.update_data(dict(type=callback.data.split('_')[2]))
        case "Client":
            await state.set_state(StatesAdmin.inputPhone)
            text += "клиента"
        case "Food":
            await state.set_state(StatesAdmin.inputPrice)
            text += "блюда"
        case "Recipe":
            await state.set_state(StatesAdmin.inputEnd)
            text = "Введите содержимое рецепта"
    await bot.send_message(callback.from_user.id, text, reply_markup=markup)


@router.message(StatesAdmin.inputFood)
async def input_name(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите ид блюда", reply_markup=markup)
    await state.set_state(StatesAdmin.inputClient)
    await state.update_data(dict(name=message.text))


@router.message(StatesAdmin.inputPhone)
async def input_food(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите номер клиента", reply_markup=markup)
    await state.set_state(StatesAdmin.inputEnd)
    await state.update_data(dict(name=message.text))


@router.message(StatesAdmin.inputClient)
async def input_food(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите ид клиента", reply_markup=markup)
    await state.set_state(StatesAdmin.inputEmployee)
    await state.update_data(dict(food_id=message.text))


@router.message(StatesAdmin.inputEmployee)
async def input_client(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите ид сотрудника", reply_markup=markup)
    await state.set_state(StatesAdmin.inputPrice)
    await state.update_data(dict(client_id=message.text))


@router.message(StatesAdmin.inputPrice)
async def input_employee(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите цену", reply_markup=markup)
    match data["class_name"]:
        case "Order":
            if data["type"] == "delivery":
                await state.set_state(StatesAdmin.inputEnd)
            else:
                await state.set_state(StatesAdmin.inputAddress)
            await state.update_data(dict(employee_id=message.text))
        case "Food":
            await state.set_state(StatesInfo.inputRecipe)
            await state.update_data(dict(name=message.text))


@router.message(StatesAdmin.inputAddress)
async def input_client(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите адрес доставки", reply_markup=markup)
    await state.set_state(StatesAdmin.inputEnd)
    await state.update_data(dict(price=message.text))


@router.message(StatesInfo.inputRecipe)
async def input_client(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    await bot.send_message(message.from_user.id, "Введите ид рецепта", reply_markup=markup)
    await state.set_state(StatesAdmin.inputEnd)
    await state.update_data(dict(price=message.text))


""" HERE WE WRITE THIS TO DB """


@router.message(StatesAdmin.inputEnd)
async def input_employee(message: Message, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    data = await state.get_data()
    class_name = data["class_name"]
    data.pop("class_name")
    match class_name:
        case "Order":
            if data["type"] == "delivery":
                await state.update_data(dict(address=message.text))
            else:
                await state.update_data(dict(price=message.text))
        case "Food":
            await state.update_data(dict(recipe_id=message.text))
        case "Client":
            await state.update_data(dict(phone=message.text))
        case "Recipe":
            await state.update_data(dict(content=message.text))
        case _:
            pass
    data = await state.get_data()
    db.add(eval(class_name)(**data))
    db.commit()
    await state.clear()
    await bot.send_message(message.from_user.id, "Успешно добавлено!", reply_markup=markup)


""" HERE WE GOT ALL OBJS TO CHECK FROM DB """


@router.callback_query(F.data.startswith('check_'))
async def obj_checkout(callback: CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()
    class_name = callback.data.split('_')[1]
    filter_dict = {}
    if class_name == "Order":
        filter_dict = {"type": callback.data.split('_')[2]}
    for obj in db.query(eval(class_name)).filter_by(**filter_dict).order_by(desc(eval(class_name).id)).limit(10).all():
        builder.button(text=str(obj), callback_data=f'info_{class_name}_{obj.id}')
    builder.adjust(2, 2)
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    builder.attach(InlineKeyboardBuilder.from_markup(markup))
    await bot.send_message(callback.from_user.id, "Выберите из списка ниже", reply_markup=builder.as_markup())


""" HERE WE GOT INFO ABOUT OBJ USER SELECTED """


@router.callback_query(F.data.startswith("info_"))
async def info_obj(callback: CallbackQuery) -> None:
    class_id = callback.data.split('_')[2]
    class_name = callback.data.split('_')[2]
    obj = db.get(eval(class_name), int(class_id))
    kb: list
    markup = InlineKeyboardBuilder()
    text = ''
    obj_keys = eval(class_name).__table__.columns.keys()
    obj_keys.remove("id")
    match class_name:
        case "Order":
            if obj.type == "dropoff":
                obj_keys.remove("address")
            obj_keys.remove("deliver_date")
            obj_keys.remove("date")
            obj_keys.remove("is_active")
        case "Recipe":
            obj_keys.remove("food")
    for key in obj_keys:
        if isAdmin(callback.from_user.id):
            markup.add(InlineKeyboardButton(text=f"Изменить поле {key}",
                                            callback_data=f"change-{class_name}-{class_id}-{key}"))
        text += f"Поле {key} - {getattr(obj, key)}\n"
    markup.adjust(2, 2)
    if class_name == "Order":
        if isAdmin(callback.from_user.id):
            markup_send_order = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Отправить заказ повару',
                                                       callback_data=f'send_toCooking-{class_id}')]])
            markup.attach(InlineKeyboardBuilder.from_markup(markup_send_order))
        markup_change_status = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Изменить статус',
                                                       callback_data=f'status_change_{class_id}')]])
        markup.attach(InlineKeyboardBuilder.from_markup(markup_change_status))
    markup_back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='go_back')]])
    markup.attach(InlineKeyboardBuilder.from_markup(markup_back))
    text += "Желаете что-то сделать?"
    await bot.send_message(callback.from_user.id, text=text, reply_markup=markup.as_markup())


""" HERE WE UPDATE DATA TO OBJ """


@router.callback_query(F.data.startswith("change-"))
async def change_client(callback: CallbackQuery, state: FSMContext) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data='go_back')]])
    await bot.send_message(callback.from_user.id, "Введите данные", reply_markup=markup)
    await state.set_state(StatesAdmin.input_info)
    await state.set_data(dict(field=callback.data.split('-')[3],
                              class_id=callback.data.split('-')[2],
                              class_name=callback.data.split('-')[1]))


@router.message(StatesAdmin.input_info)
async def input_info(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    field = data["field"]
    class_id = data["id"]
    class_name = data["class_name"]
    obj = db.get(eval(class_name), int(class_id))
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В меню", callback_data='go_back')]])
    if obj:
        if hasattr(eval(class_name), field):
            setattr(obj, field, message.text)
            db.add(obj)
            db.commit()
            await bot.send_message(message.from_user.id, "Данные внесены", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "Данные не внесены", reply_markup=markup)
    else:
        await bot.send_message(message.from_user.id, "Данные не внесены", reply_markup=markup)


""" HERE ADMIN CAN SEND ORDER TO COOKING """


@router.callback_query(F.data.startswith("send_toCooking"))
async def send_cooking(callback: CallbackQuery) -> None:
    order_id = callback.data.split('-')[1]
    kb = [[InlineKeyboardButton(text="Изменить статус", callback_data=f'status_change_{order_id}'),
           InlineKeyboardButton(text="В меню", callback_data='go_back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    order = db.get(Order, order_id)
    employee = db.get(Employee, order.employee_id)
    food = db.get(Food, order.food_id)
    recipe = db.get(Recipe, food.recipe_id)
    text = (f"Заказ - {order.name}\n"
            f"Блюдо - {food.name}\n"
            f"Рецепт - {recipe.content}\n"
            f"Цена - {order.price}")
    await bot.send_message(employee.telegram_id, text, reply_markup=markup)


""" HERE WE CAN CHANGE STATUS"""


@router.callback_query(F.data.startswith("status_change_"))
async def choose_status(callback: CallbackQuery) -> None:
    order_id = callback.data.split('_')[2]
    order = db.get(Order, order_id)
    kb = [[InlineKeyboardButton(text="В готове", callback_data=f'set_status_{order_id}_Cooking'),
           InlineKeyboardButton(text="Собран", callback_data=f'set_status_{order_id}_Package'),
           InlineKeyboardButton(text="Готов", callback_data=f'set_status_{order_id}_Done'), ], ]
    if order.type == "delivery":
        kb.append([InlineKeyboardButton(text="Передан в доставку", callback_data=f'set_status_{order_id}_Delivery'),
                   InlineKeyboardButton(text="Доставлен", callback_data=f'set_status_{order_id}_Delivered')])
    else:
        kb.append(
            [InlineKeyboardButton(text="Клиент забрал заказ", callback_data=f'set_status_{order_id}_Dropoff done')])
    kb.append([InlineKeyboardButton(text="В меню", callback_data='go_back')])
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Какой текущий статус у заказа?", reply_markup=markup)


@router.callback_query(F.data.startswith("set_status_"))
async def set_status(callback: CallbackQuery) -> None:
    order_id = callback.data.split('_')[2]
    status = callback.data.split('_')[3]
    order = db.get(Order, int(order_id))
    order.status = status
    db.add(order)
    db.commit()
    kb = [[InlineKeyboardButton(text="В меню", callback_data='go_back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(callback.from_user.id, "Статус изменён!", reply_markup=markup)
