from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.errors import (
    ApiIdInvalid as PyroApiIdInvalid,
    PhoneNumberInvalid as PyroPhoneNumberInvalid,
    PhoneCodeInvalid as PyroPhoneCodeInvalid,
    PhoneCodeExpired as PyroPhoneCodeExpired,
    SessionPasswordNeeded as PyroSessionPasswordNeeded,
    PasswordHashInvalid as PyroPasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError as TeleApiIdInvalid,
    PhoneNumberInvalidError as TelePhoneNumberInvalid,
    PhoneCodeInvalidError as TelePhoneCodeInvalid,
    PhoneCodeExpiredError as TelePhoneCodeExpired,
    SessionPasswordNeededError as TeleSessionPasswordNeeded,
    PasswordHashInvalidError as TelePasswordHashInvalid
)
from asyncio.exceptions import TimeoutError
import config

# Button configurations
ask_ques = "» Please select a platform to generate a session:"
buttons_ques = [
    [
        InlineKeyboardButton("Pyrogram", callback_data="pyrogram1"),
        InlineKeyboardButton("Pyrogram v2", callback_data="pyrogram"),
    ],
    [
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

# /generate or related commands
@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

# Generate string session based on client selection
async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    ty = "Telethon" if telethon else "Pyrogram"
    ty += " Bot" if is_bot else ""
    if not old_pyro and not telethon:
        ty += " v2"
    
    await msg.reply(f"» Starting **{ty}** session generator...")

    user_id = msg.chat.id
    # Ask for API_ID
    api_id_msg = await bot.ask(user_id, "Please send your **API_ID** to proceed.\nClick /skip to use default Bot API.", filters=filters.text)
    
    if await cancelled(api_id_msg):
        return

    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await msg.reply("API_ID must be an integer. Please try generating the session again.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "Now, send your **API_HASH** to continue.", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    
    # Ask for phone number or bot token
    if not is_bot:
        prompt_text = "Please enter your phone number (e.g. +91 95xxxxxxXX):"
    else:
        prompt_text = "Please send your **bot token** to proceed (e.g. `12345:ABC...`):"
    
    phone_number_msg = await bot.ask(user_id, prompt_text, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    
    await msg.reply(f"Trying to log in using {phone_number}...")

    # Initialize client
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=phone_number)
    elif old_pyro:
        client = Client("pyro_v1_session", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(":memory:", api_id=api_id, api_hash=api_hash)

    await client.connect()
    
    try:
        if not is_bot:
            if telethon:
                await client.send_code_request(phone_number)
            else:
                await client.send_code(phone_number)
    except (PyroApiIdInvalid, TeleApiIdInvalid):
        await msg.reply("Invalid API_ID and API_HASH combination. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PyroPhoneNumberInvalid, TelePhoneNumberInvalid):
        await msg.reply("The phone number is invalid. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return

    # Handle OTP
    phone_code_msg = await bot.ask(user_id, "Please send the OTP you received.", filters=filters.text, timeout=600)
    if await cancelled(phone_code_msg):
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code)
        else:
            await client.sign_in(phone_number, phone_code)
    except (PyroPhoneCodeInvalid, TelePhoneCodeInvalid):
        await msg.reply("The OTP you entered is invalid. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PyroPhoneCodeExpired, TelePhoneCodeExpired):
        await msg.reply("The OTP has expired. Please try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return

    # Export the string session
    string_session = client.session.save() if telethon else await client.export_session_string()
    await client.disconnect()

    # Send session details to the user
    session_message = f"Here is your {ty} string session:\n`{string_session}`\n**Do not share this session with anyone!**"
    await bot.send_message(user_id, session_message)

# Helper to handle cancellation
async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled the session generation process!", reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    return False
