from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from database.cities import countries,get_cities_for_country
import math

def choose_country():
    kb = InlineKeyboardBuilder()
    for country, code in countries.items():
        kb.button(text=country, callback_data=f"country_{code}")

    kb.adjust(3)  # Show 2 countries per row
    return kb.as_markup()

def choose_city(country, start=0, limit=9, current_page=1):
    kb = InlineKeyboardBuilder()

    country_code = countries.get(country)  # Convert country name to code
    if not country_code:
        return kb.as_markup()  # Return empty markup if the country is not found

    cities = get_cities_for_country(country_code)  # Fetch cities correctly
    # total_pages = (len(cities) + 8) // 9  # Calculate total pages
    total_pages = math.ceil(len(cities) / 9)
    for city in cities[start:limit]:
        kb.button(text=city, callback_data=f"location_{city.replace(' ', '_')}:{country_code}")

    kb.adjust(3)  # Arrange buttons in 3 columns

    pagination_buttons = []
    if current_page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text='⏪Previous page',
                                 callback_data=f'prev_page:{country}:{start}:{limit}:{current_page}')
        )

    pagination_buttons.append(InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='current'))

    if current_page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(text='Next page ⏩',
                                 callback_data=f'next_page:{country}:{start}:{limit}:{current_page}:{total_pages}')
        )

    if pagination_buttons:
        kb.row(*pagination_buttons)

    return kb.as_markup()

def choose_news_source():
    kb = InlineKeyboardBuilder()
    kb.button(text='NewsApi', callback_data='news')
    kb.button(text='GNews', callback_data='gnews')
    kb.button(text='New York Times', callback_data='nytimes')
    kb.button(text='Guardian', callback_data='guardian')
    kb.adjust(2)
    return kb.as_markup()

def read_next_news():
    kb = InlineKeyboardBuilder()
    kb.button(text='Read Next',callback_data='next')
    return kb.as_markup()