from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

class Data:
    generate_single_button = [InlineKeyboardButton("🔥 Start Generating Session 🔥", callback_data="/generate")]

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
Hey {},

Welcome to {}

If you don't trust this bot, 
> Please stop reading this message
> Delete this chat

Still reading?
You can use me to generate Pyrogram (even version 2) and Telethon string sessions. Use the buttons below to learn more!

By @ELUpdates
    """

# Start command using the Data class
@Client.on_message(filters.command("start") & filters.private)
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=Data.START.format(msg.from_user.mention, me2),
        reply_markup=InlineKeyboardMarkup(
            [
                Data.generate_single_button,  # Start Generating Session button
                [
                    InlineKeyboardButton("sᴏᴜʀᴄᴇ", url="https://t.me/Tech_Shreyansh"),
                    InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴩᴇʀ", url="https://t.me/Tech_Shreyansh2")
                ]
            ]
        ),
        disable_web_page_preview=True,
    )


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
