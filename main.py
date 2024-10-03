import config
import time
import logging
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyromod import listen  # type: ignore
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden, ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
from config import MUST_JOIN

# Add your Data class here
class Data:
    generate_single_button = [InlineKeyboardButton("🔥 Start Generating Session 🔥", callback_data="generate")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="🏠 Return Home 🏠", callback_data="home")]
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("✨ Bot Status and More Bots ✨", url="https://t.me/ELUpdates/8")],
        [
            InlineKeyboardButton("How to Use ❔", callback_data="help"),
            InlineKeyboardButton("🎪 About 🎪", callback_data="about")
        ],
        [InlineKeyboardButton("♥ More Amazing bots ♥", url="https://t.me/ELUpdates")],
    ]

    START = """
Hey {}

Welcome to {}

If you don't trust this bot, 
> Please stop reading this message
> Delete this chat

Still reading?
You can use me to generate pyrogram (even version 2) and telethon string session. Use below buttons to learn more!

By @ELUpdates
    """

    HELP = """
✨ **Available Commands** ✨

/about - About The Bot
/help - This Message
/start - Start the Bot
/generate - Generate Session
/cancel - Cancel the process
/restart - Cancel the process
"""

    ABOUT = """
**About This Bot** 

Telegram Bot to generate Pyrogram and Telethon string session by @ELUpdates

Source Code : [Click Here](https://github.com/EL-Coders/SessionStringBot)

Framework : [Pyrogram](https://docs.pyrogram.org)

Language : [Python](https://www.python.org)

Developer : @CoderEL
    """

# Initialize Pyrogram Client
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger("pymongo").setLevel(logging.ERROR)

StartTime = time.time()
app = Client(
    "Anonymous",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="StringGenBot"),
)

# Must Join feature
@app.on_message(filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return

    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            link = f"https://t.me/{MUST_JOIN}" if MUST_JOIN.isalpha() else (await bot.get_chat(MUST_JOIN)).invite_link
            await msg.reply_photo(
                photo="https://envs.sh/WUN.jpg",
                caption=f"» Please join our channel first [𝐉𝐎𝐈𝐍]({link}) and then start me again!",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join", url=link)]]
                )
            )
            await msg.stop_propagation()
    except ChatAdminRequired:
        print(f"Please promote the bot as an admin in the MUST_JOIN chat: {MUST_JOIN}")

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_command(bot: Client, msg: Message):
    bot_info = await bot.get_me()  # Get bot info
    await msg.reply(
        text=Data.START.format(msg.from_user.first_name, f"@{bot_info.username}"),
        reply_markup=InlineKeyboardMarkup(Data.buttons)
    )

# Help command
@app.on_message(filters.command("help") & filters.private)
async def help_command(bot: Client, msg: Message):
    await msg.reply(
        text=Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# About command
@app.on_message(filters.command("about") & filters.private)
async def about_command(bot: Client, msg: Message):
    await msg.reply(
        text=Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# Handle button callbacks
@app.on_callback_query(filters.regex("generate"))
async def handle_generate_callback(bot: Client, query: CallbackQuery):
    await query.message.reply("Session generation process started...")

@app.on_callback_query(filters.regex("help"))
async def handle_help_callback(bot: Client, query: CallbackQuery):
    await query.message.reply(
        text=Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

@app.on_callback_query(filters.regex("about"))
async def handle_about_callback(bot: Client, query: CallbackQuery):
    await query.message.reply(
        text=Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# Run the bot
if __name__ == "__main__":
    print("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐒𝐭𝐫𝐢𝐧𝐠 𝐁𝐨𝐭...")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID or API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    
    bot_info = app.get_me()
    print(f"@{bot_info.username} 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐒𝐔𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘. 𝐌𝐀𝐃𝐄 𝐁𝐘 @𝙏𝙀𝘾𝙃 𝙎𝙃𝙍𝙀𝙔𝘼𝙉𝙎𝙃🤗")
    
    idle()
    app.stop()
    print("𝗕𝗢𝗧 𝗦𝗧𝗢𝗣𝗣𝗘𝗗 𝗕𝗬𝗘 𝗕𝗬𝗘 !")
