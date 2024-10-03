from os import getenv
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

# Load environment variables
load_dotenv()

# Environment variables (API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MUST_JOIN)
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_ID = int(getenv("OWNER_ID"))
MONGO_DB_URI = getenv("MONGO_DB_URI")
MUST_JOIN = getenv("MUST_JOIN", None)

# Initialize Pyrogram Client
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Function to check if user has joined MUST_JOIN group or channel
@app.on_message(filters.private, group=-1)  # Apply to private messages
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return  # If MUST_JOIN is not set, skip the check
    
    try:
        # Check if the user is a member of the group/channel
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            # Generate invite link for the group/channel
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link

            # Send a message with a button to join the group
            try:
                await msg.reply_photo(
                    photo="https://envs.sh/WUN.jpg",
                    caption=f"» First, you need to join our channel [𝐉𝐎𝐈𝐍]({link}) before using this bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Join", url=link)],
                        ]
                    )
                )
                await msg.stop_propagation()  # Stop further message processing until the user joins
            except ChatWriteForbidden:
                pass  # Can't write in the chat, skip

    except ChatAdminRequired:
        print(f"Please promote the bot as an admin in the MUST_JOIN chat: {MUST_JOIN}")

# Start command after joining group
@app.on_message(filters.command("start") & filters.private)
async def start_command(bot: Client, msg: Message):
    await msg.reply_text(f"Hello, {msg.from_user.first_name}! Welcome to the bot.")

# Running the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
