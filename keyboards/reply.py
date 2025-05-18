from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_kb():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Weather')
    kb.button(text='News')

    return kb.as_markup(resize_keyboard=True)