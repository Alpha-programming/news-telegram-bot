from aiogram.types import CallbackQuery,Message
from aiogram import Router,F
from keyboards.inline import choose_city,choose_country,read_next_news
import requests
from database.cities import countries
from database.weather import get_weather
from database.news import get_all_news,get_all_news_gnews,get_all_news_nytimes,get_all_news_guardian
from database.database import users_repo,news_repo
from datetime import datetime
router = Router()

SCORE = 1
country_codes_to_names = {code: country for country, code in countries.items()}


@router.callback_query(F.data.startswith('country_'))
async def user_selected_country(call: CallbackQuery):
    country_code = call.data.replace("country_", "")  # Extract country code (e.g., "UZ")

    if country_code not in country_codes_to_names:
        return await call.answer("Does not exist", show_alert=True)

    country_name = country_codes_to_names[country_code]  # Convert code to name

    await call.message.edit_text(
        text=f"Choose a city from this country:{country_name}",
        reply_markup=choose_city(country_name)
    )

@router.callback_query(F.data.startswith('next_page'))
async def next_page(call: CallbackQuery):
    data = call.data.split(':')

    if len(data) != 6:  # Ensure data has all required parts
        return await call.answer("Error", show_alert=True)

    _, country, start, limit, page, total_pages = data
    start, limit, page, total_pages = map(int, [start, limit, page, total_pages])


    await call.message.edit_reply_markup(
        reply_markup=choose_city(
            country=country,
            start=start + 9,
            limit=limit + 9,
            current_page=page + 1,
        )
    )

@router.callback_query(F.data.startswith('prev_page'))
async def prev_page(call: CallbackQuery):
    data = call.data
    __,country, start, finish, page = data.split(':')

    await call.message.edit_reply_markup(
        reply_markup=choose_city(
            country=country,
            start=int(start) - 9,
            limit=int(finish) - 9,
            current_page=int(page) - 1,
        )
    )


@router.callback_query(F.data.startswith('location_'))
async def user_chose_location(call: CallbackQuery):
    location = call.data.replace("location_", "").replace("_", " ")
    city, country_code = location.rsplit(":", 1)
    city = city.replace("_", " ")
    country = country_codes_to_names.get(country_code, "Unknown")
    for day in get_weather(city):
        date = day['date']
        weather_main = day['weather_main']
        weather_description = day['weather_description']
        day_temp = round(day['day_temp'],1)
        night_temp = round(day['night_temp'],1)
        feels_like_day = round(day['feels_like_day'],1)
        feels_like_night = round(day['feels_like_night'],1)
        wind_speed = day['wind_speed']
        pop = day['pop']
        clouds = day['clouds']
        humidity = day['humidity']
        min_temp = round(day['min_temp'],1)
        max_temp = round(day['max_temp'],1)

        message = f'''🌨 **Weather Forecast for {date}** 🌨
        
**Condition:** {weather_main} ({weather_description.capitalize()})
**🌡 Temperature:**
    - Day: {day_temp}°C (Feels like {feels_like_day}°C)
    - Night: {night_temp}°C (Feels like {feels_like_night}°C)
    - Min: {min_temp}°C | Max: {max_temp}°C
    
🌬 **Wind:**
    - Speed: {wind_speed} m/s
☁ **Cloud Cover:** {clouds}%
🌧 **Precipitation Probability:** {pop * 100}%
💧 **Humidity:** {humidity}%
'''
        await call.message.answer(message)

@router.callback_query(F.data.startswith('news'))
async def newsapi_source(call: CallbackQuery):
    global SCORE
    SCORE = 1

    user_id = users_repo.get_user(call.from_user.id)
    news_repo.reset_autoincrement()
    news_repo.delete_news(user_id[0])
    data_list = get_all_news()
    for data in data_list:
        name = data['source']['name']
        author = data.get('author')
        title = data.get('title')
        description = data.get('description')
        url = data.get('url')
        timestamp = data.get("publishedAt")
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        published_at = dt.strftime("%B %d, %Y at %I:%M %p")

        content = data.get('content')
        news_repo.add_news(name,author,title,description,url,published_at,content,user_id[0])

    data = news_repo.get_news(user_id[0])
    news_item = data[0]
    text = (
        f"📰 **Source**: {news_item[0]}\n"
        f"📰 **Author**: {news_item[1]}\n"
        f"📅 **Published At**: {news_item[5]}\n"
        f"🏷 **Title**: {news_item[2]}\n\n"
        f"📜 **Description**: {news_item[3]}\n\n"
        f"📝 **Content**: {news_item[6]}\n"
        f"🔗 If you want to read more, please press the link below."
    )

    await call.message.edit_text(text=f'{text}')
    await call.message.answer(text=f'{data[0][4]}',reply_markup=read_next_news())

@router.callback_query(F.data.startswith('next'))
async def give_next_news(call: CallbackQuery):
    global SCORE
    user_id = users_repo.get_user(call.from_user.id)
    data = news_repo.get_news(user_id[0])

    if not data:
        await call.message.answer(text="No news available.")
        return

    if SCORE >= len(data):
        await call.message.answer(text="Sorry News in this Source has finished try to read from another source or come back later.")
        return

    news_item = data[SCORE]

    try:
        text = (
            f"📰 **Source**: {news_item[0]}\n"
            f"📰 **Author**: {news_item[1]}\n"
            f"📅 **Published At**: {news_item[5]}\n"
            f"🏷 **Title**: {news_item[2]}\n\n"
            f"📜 **Description**: {news_item[3]}\n\n"
            f"📝 **Content**: {news_item[6]}\n"
            f"🔗 If you want to read more, please press the link below."
        )

        await call.message.answer(text=text)
        await call.message.answer(text=f"{news_item[4]}", reply_markup=read_next_news())

        SCORE += 1

    except IndexError as e:
        await call.message.answer(text="Error fetching news. Please try again.")
        print(f"Error: {e}")

@router.callback_query(F.data.startswith('gnews'))
async def gnews_source(call: CallbackQuery):
    global SCORE
    SCORE = 1

    data_list = get_all_news_gnews()
    user_id = users_repo.get_user(call.from_user.id)
    news_repo.reset_autoincrement()
    news_repo.delete_news(user_id[0])
    for data in data_list:
        name = data['source']['name']
        author = data.get('author')
        title = data.get('title')
        description = data.get('description')
        url = data.get('url')
        timestamp = data.get("publishedAt")
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        published_at = dt.strftime("%B %d, %Y at %I:%M %p")

        content = data.get('content')
        news_repo.add_news(name, author, title, description, url, published_at, content, user_id[0])

    data = news_repo.get_news(user_id[0])
    news_item = data[0]
    text = (
        f"📰 **Source**: {news_item[0]}\n"
        f"📰 **Author**: {news_item[1]}\n"
        f"📅 **Published At**: {news_item[5]}\n"
        f"🏷 **Title**: {news_item[2]}\n\n"
        f"📜 **Description**: {news_item[3]}\n\n"
        f"📝 **Content**: {news_item[6]}\n"
        f"🔗 If you want to read more, please press the link below."
    )

    await call.message.edit_text(
        text=f'{text}')
    await call.message.answer(text=f'{data[0][4]}', reply_markup=read_next_news())

@router.callback_query(F.data.startswith('nytimes'))
async def nytimes_source(call: CallbackQuery):
    global SCORE
    SCORE = 1

    user_id = users_repo.get_user(call.from_user.id)
    news_repo.reset_autoincrement()
    news_repo.delete_news(user_id[0])
    data_list = get_all_news_nytimes()
    for data in data_list:
        name = data['subsection']
        author = data.get('byline')
        title = data.get('title')
        description = data.get('description')
        url = data.get('url')
        timestamp = data.get("published_date")
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
        published_at = dt.strftime("%B %d, %Y at %I:%M %p")

        content = data.get('abstract')
        news_repo.add_news(name, author, title, description, url, published_at, content, user_id[0])

    data = news_repo.get_news(user_id[0])
    news_item = data[0]
    text = (
        f"📰 **Source**: {news_item[0]}\n"
        f"📰 **Author**: {news_item[1]}\n"
        f"📅 **Published At**: {news_item[5]}\n"
        f"🏷 **Title**: {news_item[2]}\n\n"
        f"📜 **Description**: {news_item[3]}\n\n"
        f"📝 **Content**: {news_item[6]}\n"
        f"🔗 If you want to read more, please press the link below."
    )

    await call.message.edit_text(text=f'{text}')
    await call.message.answer(text=f'{data[0][4]}', reply_markup=read_next_news())

@router.callback_query(F.data.startswith('guardian'))
async def guardian_source(call: CallbackQuery):
    global SCORE
    SCORE = 1

    user_id = users_repo.get_user(call.from_user.id)
    news_repo.reset_autoincrement()
    news_repo.delete_news(user_id[0])
    data_list = get_all_news_guardian()

    for data in data_list:
        name = data.get('sectionName')
        author = data['fields']['byline']
        title = data.get('webTitle')
        description = data['fields']['headline']
        url = data.get('webUrl')
        timestamp = data.get("webPublicationDate")
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
        published_at = dt.strftime("%B %d, %Y at %I:%M %p")

        content = data['fields']['trailText']
        news_repo.add_news(name, author, title, description, url, published_at, content, user_id[0])

    data = news_repo.get_news(user_id[0])
    news_item = data[0]
    text = (
        f"📰 **Source**: {news_item[0]}\n"
        f"📰 **Author**: {news_item[1]}\n"
        f"📅 **Published At**: {news_item[5]}\n"
        f"🏷 **Title**: {news_item[2]}\n\n"
        f"📜 **Description**: {news_item[3]}\n\n"
        f"📝 **Content**: {news_item[6]}\n"
        f"🔗 If you want to read more, please press the link below."
    )

    await call.message.edit_text(text=f'{text}')
    await call.message.answer(text=f'{data[0][4]}', reply_markup=read_next_news())
