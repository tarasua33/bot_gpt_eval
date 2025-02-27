import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from src.User import User
from src.configs.configs import CLASSES, ALL_TOPICS, LLM_URL, LLM_API, TG_TOKEN
from openai import AsyncOpenAI

LLM_API_CLIENT = AsyncOpenAI(api_key=LLM_API, base_url=LLM_URL)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

user_state: {str: User} = {}


async def start_handler(message: Message):
    user = user_state.setdefault(message.from_user.id, User(LLM_API_CLIENT, message.from_user.id))
    await message.answer(user.get_greetings(), reply_markup=user.get_main_menu())


# handler /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await start_handler(message)


# handler class
@dp.message(lambda message: message.text in CLASSES)
async def choose_option(message: Message):
    user: User = user_state.get(message.from_user.id)
    user.generate_topics(message.text)
    await message.answer(user.get_topics_text(), reply_markup=user.get_topics_menu())


# handler topic
@dp.message(lambda message: message.text in ALL_TOPICS)
async def choose_topic(message: Message):
    user: User = user_state.get(message.from_user.id)
    success = await user.generate_questions(message.text)

    if success:
        await message.answer(user.get_question(), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Щось пішло не так, запустіть бот ще раз", reply_markup=ReplyKeyboardRemove())


# handler answers
@dp.message(lambda message: message.from_user.id in user_state)
async def receive_answer(message: Message):
    user: User = user_state.get(message.from_user.id)

    if user is not None:
        user.add_to_answers(message.text)

        if user.is_active_questions:
            await message.answer(user.get_question(), reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(await user.get_result(), reply_markup=ReplyKeyboardRemove())
            await user.report_result()
    else:
        await start_handler(message)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Видаляємо очікуючі оновлення
    # dp.include_router(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
