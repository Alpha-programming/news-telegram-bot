from aiogram import Router,F
from aiogram.types import Message
from keyboards.inline import choose_country,choose_news_source

router = Router()
@router.message(F.text == 'Weather')
async def weather(message: Message):
    await message.reply(text='Choose a country', reply_markup=choose_country())

@router.message(F.text == 'News')
async def news(message: Message):
    await message.reply(text='Choose a source to read news',reply_markup=choose_news_source())