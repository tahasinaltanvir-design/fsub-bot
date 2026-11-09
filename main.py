import logging
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

logging.basicConfig(level=logging.INFO)

API_ID = 24872124
API_HASH = "6f432575f63d6b0593b4a2c0c7a523b0"
BOT_TOKEN = "9174331696:AAEQqadAVKZG8pB4PxIs8QokRZB8mFMgN7U"

CHANNEL_ID = -1004484306946
GROUP_ID = -1003876095127
CHANNEL_INVITE_LINK = "https://t.me/multi_verse0"

app = Client(
    "fsub_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.chat(GROUP_ID) & ~filters.service & ~filters.me)
async def check_subscription(client, message):
    if not message.from_user:
        return
    
    user_id = message.from_user.id
    
    try:
        member = await client.get_chat_member(GROUP_ID, user_id)
        if member.status in ["administrator", "creator"]:
            return
    except Exception:
        pass

    try:
        await client.get_chat_member(CHANNEL_ID, user_id)
    except UserNotParticipant:
        try:
            await message.delete()
        except Exception:
            pass
        
        try:
            await client.restrict_chat_member(
                chat_id=GROUP_ID,
                user_id=user_id,
                permissions=pyrogram.types.ChatPermissions(can_send_messages=False)
            )
        except Exception:
            pass

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("জয়েন করুন", url=CHANNEL_INVITE_LINK)]
        ])
        
        await client.send_message(
            chat_id=GROUP_ID,
            text=f"হ্যালো [{message.from_user.first}](tg://user?id={user_id})!\n\nগ্রুপে চ্যাট করার আগে আমাদের চ্যানেলে জয়েন করতে হবে।",
            reply_markup=keyboard
        )

async def main():
    await app.start()
    print("বট সফলভাবে চালু হয়েছে এবং রান করছে...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())

