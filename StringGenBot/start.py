from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID

class Data:
    generate_single_button = [InlineKeyboardButton("★彡[ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ]彡★", callback_data="generate")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ", callback_data="home")]
    ]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ ᴀɴᴅ ᴍᴏʀᴇ ʙᴏᴛꜱ", url="https://t.me/Helpdesk_Chatsbot")],
        [
            InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ❔", callback_data="help"),
            InlineKeyboardButton("★彡[ᴀʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("sᴏᴜʀᴄᴇ", url="https://t.me/Tech_Shreyansh"),
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴩᴇʀ", url="https://t.me/Tech_Shreyansh2")
        ],
        [InlineKeyboardButton("ᴍᴏʀᴇ ᴀᴍᴀᴢɪɴɢ ʙᴏᴛꜱ", url="https://t.me/Tech_Shreyansh2")],
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

Telegram Bot to Generate Pyrogram and Telethon string session by @ʜᴇʟᴘᴅᴇꜱᴋ_ᴄʜᴀᴛꜱʙᴏᴛ

Source Code : [Click Here](https://github.com/techyshreyansh/STRING-SESSION)

Framework : [Pyrogram](https://docs.pyrogram.org)

Language : [Python](https://www.python.org)

Developer : [@ᴛᴇᴄʜ ꜱʜʀᴇʏᴀɴꜱʜ](https://t.me/Helpdesk_Chatsbot)
    """

# Filter function for commands
def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

# Start command
@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_photo(
        chat_id=msg.chat.id,
        photo="https://envs.sh/WUN.jpg",  # Replace with your image URL
        caption=f"""Hᴇʏ {msg.from_user.mention}🦋,

Tʜɪs ɪs {me2},
Aɴ ᴏᴘᴇɴ sᴏᴜʀᴄᴇ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ, ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴩʏʀᴏɢʀᴀᴍ.
ᴊɪsᴋᴇ ᴊᴀɪʙ ᴍᴇ ɢᴀɴᴅʜɪ  ᴄʜᴏʀɪ ᴜsᴋᴇ ᴘʏᴀᴀʀ ᴍᴇ ᴀᴀɴᴅʜɪ 🖤.

Mᴀᴅᴇ ᴡɪᴛʜ ❤ ʙʏ : [ᴛᴇᴄʜ ꜱʜʀʏᴀɴꜱʜ](https://t.me/Helpdesk_Chatsbot) !""",
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

# Handle Home button callback
@Client.on_callback_query(filters.regex("home"))
async def handle_home_callback(bot: Client, query: CallbackQuery):
    # Recreate the welcome message for the home menu
    me2 = (await bot.get_me()).mention
    await query.message.reply_photo(
        photo="https://envs.sh/WUN.jpg",  # Replace with your image URL
        caption=f"""Hᴇʏ {query.from_user.mention}🦋,

Tʜɪs ɪs {me2},
Aɴ ᴏᴘᴇɴ sᴏᴜʀᴄᴇ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ, ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴩʏʀᴏɢʀᴀᴍ.
ᴊɪsᴋᴇ ᴊᴀɪʙ ᴍᴇ ɢᴀɴᴅʜɪ  ᴄʜᴏʀɪ ᴜsᴋᴇ ᴘʏᴀᴀʀ ᴍᴇ ᴀᴀɴᴅʜɪ 🖤.

Mᴀᴅᴇ ᴡɪᴛʜ ❤ ʙʏ : [ᴛᴇᴄʜ ꜱʜʀʏᴀɴꜱʜ](https://t.me/Helpdesk_Chatsbot) !""",
        reply_markup=InlineKeyboardMarkup(Data.buttons),  # Display the full set of buttons
        disable_web_page_preview=True,
    )
