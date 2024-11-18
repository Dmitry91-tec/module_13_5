from aiogram import Bot, Dispatcher, executor, types            #Импортируем сущность бота, диспетчера, «executor», типы
from aiogram.contrib.fsm_storage.memory import MemoryStorage    #блока работы с памятью
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "7899637913:AAE-qnqGqAZvGEeSSHLoj9cfow2EmYjVmSY"
bot = Bot(token = api)                                  #Дальше понадобится api ключ, который мы получили в «BotFather». Так же переменная бота, она будет хранить объект бота, «token» будет равен вписанному ключу
dp = Dispatcher(bot, storage = MemoryStorage())          #Понадобится «Dispatcher», который будет объектом «Dispatcher», у него будет наш бот в качестве аргументов. В качестве «Storage» будет «MemoryStorage»

kb = ReplyKeyboardMarkup(resize_keyboard=True)                              #инициализируем клавиатуру
button_1 = KeyboardButton(text = "Рассчитать")
button_2 = KeyboardButton(text = 'Информация')
kb.row(button_1)                                         #добавим кнопки в клавиатуру
kb.row(button_2)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет", reply_markup = kb)   #позволяет отображать клавиатуру


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer("Введите свой возраст:")               #ожидание получения сообщения от пользователя
    await UserState.age.set()                                   #для установки состояния и записи адреса

@dp.message_handler(state=UserState.age)                       #обработано не обычным хендлером, а хендлером состояния «@dp.message_handler()».
async def set_growth(message, state):                          #когда хендлер сработает, вы получите два объекта: «message» и «state», который представляет текущее состояние пользователя
    await state.update_data(first=message.text)                             #позволяет обновить данные, связанные с текущим состоянием пользователя
    data = await state.get_data()                                    #метод позволяет вернуть все данные, связанные с текущим состоянием пользователя
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)                   # обработано не обычным хендлером, а хендлером состояния «@dp.message_handler()».
async def set_weight(message,state):                   # когда хендлер сработает, вы получите два объекта: «message» и «state», который представляет текущее состояние пользователя
    await state.update_data(second=message.text)            # позволяет обновить данные, связанные с текущим состоянием пользователя
    data = await state.get_data()                          # метод позволяет вернуть все данные, связанные с текущим состоянием пользователя
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)               # обработано не обычным хендлером, а хендлером состояния «@dp.message_handler()».
async def send_calories(message,state):                   # когда хендлер сработает, вы получите два объекта: «message» и «state», который представляет текущее состояние пользователя
    await state.update_data(third=message.text)           # позволяет обновить данные, связанные с текущим состоянием пользователя
    data = await state.get_data()                         # метод позволяет вернуть все данные, связанные с текущим состоянием пользователя
    result=round(10*int(data['first']) + 6,25*int(data['second'])-5*int(data['third']) + 5)
    await message.answer(result)
    await UserState.weight.set()
    await state.finish()                                                   #машина состояний завершила работу, ее необходимо закрыть с помощью метода



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)          #Запускаем «executor», у которого есть функция «start_polling». Объясняем, через кого ему запускаться
