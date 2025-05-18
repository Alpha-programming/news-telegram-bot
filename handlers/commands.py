from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart,Command
from keyboards.reply import start_kb
from database.database import users_repo

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    chat_id = message.from_user.id
    users_repo.add_user(chat_id=chat_id)
    await message.answer('Welcome to the Weather Bot',reply_markup=start_kb())

@router.message(Command(commands='info'))
async def info(message: Message):
    await message.answer(text='This bot is used to provide daily weather forecast for 10 days ahead.\nMoreover it can provide daily news which can be taken in 4 sources to provide you with brief data and link to its full content.')
