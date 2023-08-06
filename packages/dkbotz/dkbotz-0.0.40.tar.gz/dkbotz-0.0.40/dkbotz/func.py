# Bot By https://t.me/DKBOTZ || https://t.me/DK_BOTZ || https://t.me/DKBOTZHELP
# Creadit To My Friend https://t.me/Bot_Magic_World


import requests
import re, random, asyncio 
from os import environ
from .imdb import get_movie_info

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

PICS = (environ.get('PICS', 'https://telegra.ph/file/7e56d907542396289fee4.jpg https://telegra.ph/file/9aa8dd372f4739fe02d85.jpg https://telegra.ph/file/adffc5ce502f5578e2806.jpg https://telegra.ph/file/6937b60bc2617597b92fd.jpg https://telegra.ph/file/09a7abaab340143f9c7e7.jpg https://telegra.ph/file/5a82c4a59bd04d415af1c.jpg https://telegra.ph/file/323986d3bd9c4c1b3cb26.jpg https://telegra.ph/file/b8a82dcb89fb296f92ca0.jpg https://telegra.ph/file/31adab039a85ed88e22b0.jpg https://telegra.ph/file/c0e0f4c3ed53ac8438f34.jpg https://telegra.ph/file/eede835fb3c37e07c9cee.jpg https://telegra.ph/file/e17d2d068f71a9867d554.jpg https://telegra.ph/file/8fb1ae7d995e8735a7c25.jpg https://telegra.ph/file/8fed19586b4aa019ec215.jpg https://telegra.ph/file/8e6c923abd6139083e1de.jpg https://telegra.ph/file/0049d801d29e83d68b001.jpg')).split()

FILTER_DEL_SECOND = 600
API_KEY = 'True'

async def group_filters(client, update, temp, get_filter_results, get_size, split_list, get_settings, caption_text):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return
    if 2 < len(update.text) < 100:    
        btn = []
        search = update.text
        settings = await get_settings(update.chat.id)
        MOVIE_TEXT = settings["template"]
        files = await get_filter_results(query=search)
        if not files:
            if settings["spellmode"]:
                try:
                    reply = search.replace(" ", '+')  
                    buttons = [[ InlineKeyboardButton("🔍 𝚂𝙴𝙰𝚁𝙲𝙷 𝚃𝙾 𝙶𝙾𝙾𝙶𝙻𝙴 🔎", url=f"https://www.google.com/search?q={reply}") ],[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]]
                    spell = await update.reply_text(text=settings["spelltext"].format(query=search, first_name=update.from_user.first_name, last_name=update.from_user.last_name, title=update.chat.title, mention=update.from_user.mention), disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))           
                    await asyncio.sleep(60)
                    await spell.delete()
                except:
                    pass
            return
        if files:
            for file in files:
                file_id = file.file_id
                filesize = f"[{get_size(file.file_size)}]"
                botusername= await client.get_me()
                filename = f"{file.file_name}"
                settings = await get_settings(update.chat.id)
                API = settings["api"] if settings["api"] else 'UsdyUrWdP9Mt2tPbxTVSbsfM4hu2' # UsdyUrWdP9Mt2tPbxTVSbsfM4hu2
                resp = requests.get(f'https://api.shareus.in/shortLink?token={API}&format=json&link=https://t.me/{botusername.username}?start=DKBOTZ-DK-BOTZ-{file_id}').json()
                if resp['status'] == 'success':
                    url = resp['shortlink']
                if settings["button"]:
                    btn.append([InlineKeyboardButton(f"{filesize} {filename}", url=url)])
                else:                    
                    btn.append([InlineKeyboardButton(f"{filesize}", url=url),
                                InlineKeyboardButton(f"{filename}", url=url)])
        else:
            return

        if not btn:
            return

        if len(btn) > temp.filterBtns: 
            btns = list(split_list(btn, temp.filterBtns)) 
            keyword = f"{update.chat.id}-{update.id}"
            temp.BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append([InlineKeyboardButton("📃 Pages 1/1",callback_data="pages"),
                            InlineKeyboardButton("Close 🗑️", callback_data="close")])

            buttons.append([InlineKeyboardButton("🤖 𝙲𝙷𝙴𝙲𝙺 𝙼𝚈 𝙿𝙼 🤖", url=f"https://telegram.dog/{temp.Bot_Username}?")])

            try:             
                if settings["photo"]:
                    movie_name = update.text
                    movie_info = get_movie_info(movie_name)
                    if movie_info:
                        poster = movie_info["pimage"]
                    
    
                    try:
                        query = search
                        movie_title = movie_info['title']
                        Rating = movie_info['imdb_rating']
                        Year = movie_info['release']
                        Genres = movie_info['genre']
                        Runtime = movie_info['duration']
                        Countries = movie_info['country']
                        director = movie_info['director']
                        writer = movie_info['writer']
                        BoxOffice = movie_info['BoxOffice']
                        language = movie_info['language']
                        votes = movie_info['votes']
                        mention = update.from_user.mention
                        greeting = None
                        remove = await update.reply_photo(photo=poster, caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                        await asyncio.sleep(FILTER_DEL_SECOND)
                        await remove.delete()
                    except:
                        remove = await update.reply_photo(photo=random.choice(PICS), caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                        await asyncio.sleep(FILTER_DEL_SECOND)
                        await remove.delete()
                else:
                    try:
                        remove = await update.reply_photo(photo=random.choice(PICS), caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                        await asyncio.sleep(FILTER_DEL_SECOND)
                        await remove.delete()
                    except:
                        remove = await update.reply_photo(photo=random.choice(PICS), caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                        await asyncio.sleep(FILTER_DEL_SECOND)
                        await remove.delete()
            except:
                remove = await update.reply_photo(photo=random.choice(PICS), caption=MOVIE_TEXT.format(mention=update.from_user.mention, query=search, greeting=None, group_name = f"[{update.chat.title}](t.me/{update.chat.username})" or f"[{update.chat.title}](t.me/{update.from_user.username})"), reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(FILTER_DEL_SECOND)
                await remove.delete()
            return

        data = temp.BUTTONS[keyword]
        buttons = data['buttons'][0].copy()
   
        buttons.append([InlineKeyboardButton(f"📃 1/{data['total']}",callback_data="pages"),
                        InlineKeyboardButton("🗑️", callback_data="close"),
                        InlineKeyboardButton("➡",callback_data=f"nextgroup_0_{keyword}")])

        buttons.append([InlineKeyboardButton("🤖 𝙲𝙷𝙴𝙲𝙺 𝙼𝚈 𝙿𝙼 🤖", url=f"https://telegram.dog/{temp.Bot_Username}")])

        try:             
            if settings["photo"]:
                movie_name = update.text
                movie_info = get_movie_info(movie_name)
                if movie_info:
                    poster = movie_info["pimage"]
                try:
                    query = search
                    movie_title = movie_info['title']
                    Rating = movie_info['imdb_rating']
                    Year = movie_info['release']
                    Genres = movie_info['genre']
                    Runtime = movie_info['duration']
                    Countries = movie_info['country']
                    director = movie_info['director']
                    writer = movie_info['writer']
                    language = movie_info['language']
                    votes = movie_info['votes']
                    BoxOffice = movie_info['BoxOffice']
                    mention = update.from_user.mention
                    greeting = None
                    remove = await update.reply_photo(photo=poster, caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(FILTER_DEL_SECOND)
                    await remove.delete()
                except:
                    remove = await update.reply_photo(photo=poster, caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(FILTER_DEL_SECOND)
                    await remove.delete()
            else:
                try:
                    remove = await update.reply_photo(photo=poster, caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(FILTER_DEL_SECOND)
                    await remove.delete()
                except :
                    remove = await update.reply_photo(photo=poster, caption=f"**👨‍🦱 Requested By:** {mention}\n\n**🤵‍♂️ Requested Name:** {query}\n\n🎥 **Movie Title:** {movie_title}\n\n🎭 **Genres:** {Genres}\n\n**📀 Votes:** {votes}\n\n🌟 **IMDB Rating :** {Rating}\n\n📆 **Released:**  {Year} \n\n📣 **BoxOffice:** {BoxOffice}\n\n**🧑‍💻 Writer:** {writer}\n\n**🕺 Director:** {director}\n\n🗺️ **Countries:** {Countries}\n\n{caption_text}", reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(FILTER_DEL_SECOND)
                    await remove.delete()
        except:
            remove = await update.reply_photo(photo=random.choice(PICS), caption=MOVIE_TEXT.format(mention=update.from_user.mention, query=search, greeting=None, group_name = f"[{update.chat.title}](t.me/{update.chat.username})" or f"[{update.chat.title}](t.me/{update.from_user.username})"), reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(FILTER_DEL_SECOND)
            await remove.delete()
