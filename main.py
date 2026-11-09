import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "9174331696:AAEQqadAVKZG8pB4PxIs8QokRZB8mFMgN7U"
CHANNEL_ID = -1004484306946
GROUP_ID = -1003876095127
CHANNEL_INVITE_LINK = "https://t.me/multi_verse0"

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    
    if not message or not user or message.chat.id != GROUP_ID:
        return

    # অ্যাডমিন চেক
    try:
        chat_member = await context.bot.get_chat_member(chat_id=GROUP_ID, user_id=user.id)
        if chat_member.status in ["administrator", "creator"]:
            return
    except TelegramError:
        pass

    # চ্যানেলে সাবস্ক্রাইব করা আছে কিনা চেক
    is_member = False
    try:
        member_status = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
        if member_status.status in ["member", "administrator", "creator"]:
            is_member = True
    except TelegramError:
        pass

    if not is_member:
        try:
            await message.delete()
        except TelegramError:
            pass
        
        try:
            await context.bot.restrict_chat_member(
                chat_id=GROUP_ID,
                user_id=user.id,
                permissions=ChatPermissions(can_send_messages=False)
            )
        except TelegramError:
            pass

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("চ্যানেলে জয়েন করুন", url=CHANNEL_INVITE_LINK)
        ]])
        
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=f"হ্যালো [{user.first_name}](tg://user?id={user.id})!\n\nগ্রুপে মেসেজ পাঠানোর আগে আমাদের চ্যানেলে জয়েন করতে হবে।",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, check_subscription))
    
    print("বট সফলভাবে চালু হয়েছে...")
    application.run_polling()

if __name__ == "__main__":
    main()
