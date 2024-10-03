from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID

class Data:
    generate_single_button = [InlineKeyboardButton("🔥 Start Generating Session 🔥", callback_data="generate")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="🏠 Return Home 🏠", callback_data="home")]
    ]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("✨ Bot Status and More Bots ✨", url="https://t.me/ELUpdates/8")],
        [
            InlineKeyboardButton("How to Use ❔", callback_data="help"),
            InlineKeyboardButton("🎪 About 🎪", callback_data="about")
        ],
        [InlineKeyboardButton("♥ More Amazing bots ♥", url="https://t.me/ELUpdates")],
    ]

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

# Filter function for commands
def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

# Start command
@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""Hᴇʏ {msg.from_user.mention}🦋,

Tʜɪs ɪs {me2},
Aɴ ᴏᴘᴇɴ sᴏᴜʀᴄᴇ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ, ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴩʏʀᴏɢʀᴀᴍ.
ᴊɪsᴋᴇ ᴊᴀɪʙ ᴍᴇ ɢᴀɴᴅʜɪ  ᴄʜᴏʀɪ ᴜsᴋᴇ ᴘʏᴀᴀʀ ᴍᴇ ᴀᴀɴᴅʜɪ 🖤.

Mᴀᴅᴇ ᴡɪᴛʜ ❤ ʙʏ : [ʙᴀʀɴᴅᴇᴅ ᴋɪɴɢ](https://t.me/BRANDEDKING8) !""",
        reply_markup=InlineKeyboardMarkup(Data.buttons),  # Use the full set of buttons
        disable_web_page_preview=True,
    )

# Help command
@Client.on_message(filters.command("help") & filters.private)
async def help_command(bot: Client, msg: Message):
    await msg.reply(
        text=Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# About command
@Client.on_message(filters.command("about") & filters.private)
async def about_command(bot: Client, msg: Message):
    await msg.reply(
        text=Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

# Handle button callbacks
@Client.on_callback_query(filters.regex("generate"))
async def handle_generate_callback(bot: Client, query: CallbackQuery):
    await query.message.reply("Session generation process started...")

@Client.on_callback_query(filters.regex("help"))
async def handle_help_callback(bot: Client, query: CallbackQuery):
    await query.message.reply(
        text=Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )

@Client.on_callback_query(filters.regex("about"))
async def handle_about_callback(bot: Client, query: CallbackQuery):
    await query.message.reply(
        text=Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )
