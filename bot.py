import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# 🔐 BOT TOKEN & CHANNEL ID will come from GitHub Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

DATABASE = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============= CHANNEL WATCHER =============
async def channel_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.caption:
        caption = update.channel_post.caption.lower()

        if "code:" in caption:
            code = caption.split("code:")[1].strip()
            DATABASE[code] = update.channel_post.message_id
            print(f"SAVED => {code} → msg_id {update.channel_post.message_id}")


# ============= USER /start =============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Welcome!**\n"
        "Yaha file unlock karne ke liye bas code bhejo.\n\n"
        "📢 Hamara Channel Join Karo:\n"
        "👉 https://t.me/tm_jam_nagar\n\n"
        "Code bhejo file mil jayegi 😊"
    )


# ============= USER CODE =============
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.strip().lower()

    if user_code in DATABASE:
        msg_id = DATABASE[user_code]

        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=msg_id
        )
        return

    await update.message.reply_text("❌ Galat code. Sahi code bhejo.")


# ============= MAIN =============
def main():
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN not found! GitHub Secrets me add karo.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, channel_update))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    print("🤖 BOT STARTED SUCCESSFULLY & Watching Channel…")

    app.run_polling()


if __name__ == "__main__":
    main()