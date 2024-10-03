import config
import time
import logging
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

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

# Can't write in the chat, skip

if __name__ == "__main__":
    print("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐒𝐭𝐫𝐢𝐧𝐠 𝐁𝐨𝐭...")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    uname = app.get_me().username
    print(f"@{uname} 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐒𝐔𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘. 𝐌𝐀𝐃𝐄 𝐁𝐘 @𝙏𝙀𝘾𝙃 𝙎𝙃𝙍𝙀𝙔𝘼𝙉𝙎𝙃🤗")
    idle()
    app.stop()
    print("𝗕𝗢𝗧 𝗦𝗧𝗢𝗣𝗣𝗘𝗗 𝗕𝗬 𝗕𝗬 !")
