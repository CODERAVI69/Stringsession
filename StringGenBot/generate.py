from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config

ask_ques = "» Please choose an option to generate your session:"
buttons_ques = [
    [
        InlineKeyboardButton("Pyrogram v2", callback_data="pyrogram"),
        InlineKeyboardButton("Telethon", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("Pyrogram Bot", callback_data="pyrogram_bot"),
        InlineKeyboardButton("Telethon Bot", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="Generate Session", callback_data="generate")
    ]
]

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "Telethon"
    else:
        ty = "Pyrogram"
        if not old_pyro:
            ty += " v2"
    if is_bot:
        ty += " Bot"
    
    await msg.reply(f"Starting **{ty}** session generator...")
    user_id = msg.chat.id
    
    # Get API ID and API Hash
    api_id_msg = await bot.ask(user_id, "Please send your **API_ID** to proceed.\n\nClick on /skip to use default Bot API.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("API_ID must be an integer. Please try again.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        
        api_hash_msg = await bot.ask(user_id, "Now please send your **API_HASH** to continue.", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text

    # Get Phone Number or Bot Token
    if not is_bot:
        t = "Please enter your phone number (e.g., +91 XXXXXXX):"
    else:
        t = "Please send your **bot token** to continue."
    
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text

    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    
    await client.connect()

    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("Invalid API_ID and API_HASH combination. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply("The phone number is invalid. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return

    try:
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "Please send the OTP you received from Telegram.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("Timeout reached (10 minutes). Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return

    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply("Invalid OTP. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("OTP expired. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            two_step_msg = await bot.ask(user_id, "Please enter your 2FA password.", filters=filters.text, timeout=300)
            if await cancelled(two_step_msg):
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await msg.reply("Invalid 2FA password. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)

    # Session generation
    string_session = client.session.save() if telethon else await client.export_session_string()
    text = f"**Here is your {ty} string session**:\n\n`{string_session}`\n\nDo not share it with anyone!"
    
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    
    await client.disconnect()
    await bot.send_message(msg.chat.id, f"Successfully generated your {ty} string session. Check your saved messages.")

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled the session generation process.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    return False
