import math
import time
import asyncio

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserBannedInChannel, UserNotParticipant


#Forcesub
async def force_sub(c, m, channel, ft):
    try:
        CHANNEL = channel
        chat = await c.get_chat_member(CHANNEL, m.from_user.id)
        if chat.status=='kicked':
            await m.reply_text('**Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/DKBOTZSUPPORT).**')
            return True

    except UserNotParticipant:
        button = [[InlineKeyboardButton('🔰 Join Now 🔰', url=f'https://t.me/{CHANNEL}')]]
        markup = InlineKeyboardMarkup(button)
        await m.reply_text(text=f"👋 Hi {m.from_user.mention(style='md')},\n\n{ft}", reply_markup=markup, disable_web_page_preview=True)
        return True

    except Exception as e:
        await m.reply_text(f"Some thing went wrong 🤔. Try Again And if Same issue Comes Then Contact [Our Support Group](https://t.me/DKBOTZSUPPORT)\n\nError :- {e}", disable_web_page_preview=True)
        return True

#Forcesub
async def force_subs(c, m, channel, ft):
    try:
        CHANNEL = channel
        chat = await c.get_chat_member(CHANNEL, m.from_user.id)
        if chat.status=='kicked':
            await m.reply_text('**Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/DKBOTZSUPPORT).**')
            return True

    except UserNotParticipant:
        button = [[InlineKeyboardButton('🔰 Join Now 🔰', url=f'https://t.me/{CHANNEL}')]]
        markup = InlineKeyboardMarkup(button)
        await m.reply_text(text=f"👋 Hi {m.from_user.mention(style='md')},\n\n{ft}\n\nAnd Also Join :- @DKBOTZ", reply_markup=markup, disable_web_page_preview=True)
        return True

    except Exception as e:
        await m.reply_text(f"Some thing went wrong 🤔. Try Again And if Same issue Comes Then Contact [Our Support Group](https://t.me/DKBOTZSUPPORT)\n\nError :- {e}", disable_web_page_preview=True)
        return True
