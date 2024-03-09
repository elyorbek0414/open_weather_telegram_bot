import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from api import create_user, create_feedback
from states import FeedbackState
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from buttons import button

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Привет!{format(message.from_user.first_name)} Напиши мне название города и я пришлю сводку погоды!")
    print(create_user(message.from_user.username, message.from_user.first_name, message.from_user.id))


@dp.message_handler(Text(startswith="🇺🇸: 𝔻𝕖𝕞𝕒𝕟𝕕 𝕒𝕟𝕕 𝕤𝕦𝕡𝕡𝕝𝕪"))
async def feedback_1(message: types.Message):
    await message.reply("Ваше мнение важно для нас!")
    await FeedbackState.body.set()


@dp.message_handler(state=FeedbackState.body)
async def feedback_2(message: types.Message, state: FSMContext):
    await message.answer(create_feedback(message.from_user.id, message.text))
    await state.finish()


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("команда в разработке\t"
                        "пока недоступна", reply_markup=button)


@dp.message_handler(commands=["about"])
async def help_command(message: types.Message):
    await message.reply('Бот создан от 𝔼𝕝𝕪𝕠𝕣𝕓𝕖𝕜 и в будущем этот бот будет самым лучшим ботом если кому то из вас хочется учить как создавать такую бот то обращайтесь к 👉🏻 @N1_6002076, @Uncharted_777 👈🏻')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"👉🏻 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} 👈🏻\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня!...\n"
              f"Ещё какого Города вы хотите узнать погоду?"
              )

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)
executor.start_polling(dp, skip_updates=True)
