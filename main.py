# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from aiogram import Bot, Dispatcher, executor, types
from wikipedia import search, summary, DisambiguationError

API_TOKEN = '123123'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nВведи название любимой команды и получишь ссылку на статью про неё в википедии)")


@dp.message_handler()
async def echo(message: types.Message):
    answer = 'По вашему запросу ничего не нашлось. Попробуйте уточнить'
    results = search(message.text, results=10, suggestion=False)
    if len(results) == 0 or len(results[0]) == 0:
        answer = 'Не удалось найти команду, попробуйте указать город'
    for result in results:
        try:
            if 'football club' in summary(result, auto_suggest=False)[:300].lower():
                answer = 'en.wikipedia.org/wiki/' + result.replace(' ', '_')
                break
        except DisambiguationError:
            answer = 'Так может называться не только команда. Пожалуйста, уточните запрос.'
            break
    await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
