"""
Telegram bot for beer inventory management.
Works alongside WhatsApp bot, sharing the same inventory data.
"""
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from commands import handle_message

load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages from Telegram."""
    try:
        # Get the message text
        message_text = update.message.text or ""
        
        # Skip empty messages
        if not message_text.strip():
            return
        
        # Get user info for logging
        user = update.message.from_user
        user_name = user.first_name or user.username or "Unknown"
        
        # Process the command
        response_text = handle_message(message_text)
        
        # Send response back (works in both groups and private chats)
        await update.message.reply_text(response_text)
        
        # Log the interaction
        chat_type = update.message.chat.type
        print(f"[Telegram {chat_type}] {user_name}: {message_text} -> {response_text}")
    except Exception as e:
        print(f"Error handling Telegram message: {str(e)}")
        import traceback
        print(traceback.format_exc())


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    welcome_message = """🍺 Welkom bij de Bier Voorraad Bot!

Deze bot beheert je bierkratten voorraad.

Beschikbare commando's:
• /status - Controleer huidige voorraad
• /commands - Zie alle beschikbare commando's

Of stuur gewoon een bericht zoals:
• "status"
• "voeg 2 kratten toe"
• "verwijder 1 krat"

Type /commands voor de volledige lijst!"""
    
    await update.message.reply_text(welcome_message)


async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /commands command."""
    commands_list = handle_message("commands")
    await update.message.reply_text(commands_list)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    status = handle_message("status")
    await update.message.reply_text(status)


def main() -> None:
    """Start the Telegram bot."""
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in .env file")
        print("Please add: TELEGRAM_BOT_TOKEN=your_token_here")
        return
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("commands", commands_command))
    application.add_handler(CommandHandler("status", status_command))
    # Handle all text messages (including in groups)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Start the bot
    print("Starting Telegram bot...")
    print(f"Bot username: @Deugnietbot")
    print("Telegram bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

