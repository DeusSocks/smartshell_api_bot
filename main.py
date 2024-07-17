from aiogram import Dispatcher, Bot, types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
import asyncio
import requests
# Введите в строчку токен тг бота
bot = Bot(token="TOKEN")
dp = Dispatcher(bot=bot)
router = Router()
# Тут нужен токен из test.py вставлять псоле bearer
BEARER_TOKEN = "Bearer TOKEN"
keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ПК", callback_data="info"),
        InlineKeyboardButton(text="Смена", callback_data="smena"),
        InlineKeyboardButton(text="Поддержка", callback_data="faq")
]],)



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global keyboard
    await message.answer("Здарова, меченый! Выбери интересующий пункт, для получения нужной информации. \n WELCOME TO THE COMPUTER CLUB ONYX, BUDDY  \n Версия 0.0.1",
                         reply_markup=keyboard)


@dp.callback_query(F.data != 'menu')
async def give_info(callback: types.CallbackQuery):
    key_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
    await callback.answer()
    url = 'https://billing.smartshell.gg/api/graphql'
    headers = {
            'Authorization': BEARER_TOKEN,
            'Content-Type': 'application/json'
        }
    if callback.data == 'info':
        body = """query Hosts {
    hosts {
        id
        group_id
        type_id
        position
        alias
        comment
        mac_addr
        ip_addr
        dns_name
        coord_x
        coord_y
        is_deleted
        in_service
        created_at
        shell_mode
        last_online
        online
        device_has_changed
        device_updated_at
        locked
        admin_called_at
        client_sessions {
            id
            duration
            elapsed
            total_cost
            status
            created_at
            started_at
            finished_at
            canceled_at
            client {
                nickname
            }
        }
    }
}"""

        response = requests.post(url, headers=headers, json={"query": body})
        #print(response.status_code)

        data = response.json()
        
        # Если нужны логи, то убираем коммент с print
        #print(data)
        
        
        text = "=================================\n"
        for el in data["data"]["hosts"]:
            #print(el)
            text += f"""ID: {el["id"]}
Место: {el["position"]}
Название: {el["alias"]}
ДНС: {el["dns_name"]}
Состояние: {el["online"]}
Юзер за ПК: {"Нет" if len(el["client_sessions"]) == 0 else "Да"}
Заверешние сеанса: {el["client_sessions"][0]["finished_at"] if len(el["client_sessions"]) != 0 else "Нету информации"}
    =================================
    """
        # Если нужны логи, то убираем коммент с print
        #print(text)

        await callback.message.answer(text,
                                      reply_markup=key_menu)

    

    elif callback.data == 'smena':
        body = """query ActiveWorkShift {
        activeWorkShift {
            id
            comment
            created_at
            finished_at
            worker {
                uuid
                login
                nickname
                phone
                email
                phone_suffix
                dob
                country_code
                first_name
                last_name
                middle_name
            }
            payments {
                sum
            }
        }
    }
            """
        body_2 = """query Hosts {
    activeWorkShift {
        id
        comment
        created_at
        finished_at
        money {
            sum {
                cash
                card
                total
            }
        }
    }
}"""
        response = requests.post(url, headers=headers, json={"query": body})
        response_2 = requests.post(url, headers=headers, json={"query": body_2})
        data = response.json()
        data_work = response_2.json()
        #print(response.status_code)

        #print(data)
        #print(data_work)
        
        text = f"""Имя:{data['data']['activeWorkShift']['worker']['first_name']}
Фамилия: {data['data']['activeWorkShift']['worker']['last_name']}
Номер телефона сотрудника:{data['data']['activeWorkShift']['worker']['phone']}
Открыл смену: {data['data']['activeWorkShift']['created_at']}
Заработок за сегодня: {data_work["data"]["activeWorkShift"]["money"]["sum"]["total"]} ₽
Наличные: {data_work["data"]["activeWorkShift"]["money"]["sum"]["cash"]} ₽
Безналичные: {data_work["data"]["activeWorkShift"]["money"]["sum"]["card"]} ₽

        """

        #print(text)
        await callback.message.answer(text,
                                      reply_markup=key_menu)

    if callback.data == 'faq':
        
        text = """===========<b>Поддержка</b>============
    <b>Поддержка - @DeusOfSocks</b>
        """

        #print(text)
        await callback.message.answer(text,
                                      reply_markup=key_menu,
                                      parse_mode="HTML")





@dp.callback_query(F.data == "menu")
async def cmd_menu(callback:types.CallbackQuery):
    global keyboard
    await callback.message.answer("Здарова, меченый! Выбери интересующий пункт, для получения нужной информации. \n WELCOME TO THE COMPUTER CLUB ONYX, BUDDY  \n Версия 0.0.1",
                         reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
