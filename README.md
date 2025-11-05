# Beer Inventory Bot (WhatsApp + Telegram)

A dual-platform bot for managing beer crate inventory for a student bar. Works on both WhatsApp (via Twilio) and Telegram, sharing the same inventory data.

## Features

- ✅ Dual-platform support: WhatsApp and Telegram
- ✅ Check current inventory
- ✅ Add/subtract crates from inventory
- ✅ Group chat support on Telegram (for visibility)
- ✅ Shared inventory data between both platforms
- ✅ Simple JSON-based storage (no database needed)
- ✅ Crate-based inventory management

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Twilio account (free tier available)
- ngrok (for local development)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Twilio WhatsApp Sandbox Setup

1. Sign up for a free Twilio account at [twilio.com](https://www.twilio.com)
2. Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Follow instructions to join the WhatsApp sandbox
4. Get your Twilio credentials:
   - Account SID
   - Auth Token
   - WhatsApp sandbox number (usually `whatsapp:+14155238886`)

### 4. Telegram Bot Setup

1. Create a Telegram bot:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow the instructions
   - Save the bot token you receive

2. Add bot to your group:
   - Create a Telegram group (or use existing)
   - Add your bot to the group: Search for `@Deugnietbot` and add it
   - **Important**: Give bot admin permissions (required for group chat)
     - Go to group settings → Administrators → Add Admin → Select your bot

### 5. Configure Environment Variables

1. Edit your `.env` file and add your credentials:
   ```
   # Twilio (WhatsApp)
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   
   # Telegram
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   
   # Inventory
   DEFAULT_CRATES=50
   ```

### 6. Expose Local Server (for Development - WhatsApp only)

1. Install ngrok: https://ngrok.com/download
2. Start the FastAPI server (see next step)
3. In a new terminal, run:
   ```bash
   ngrok http 8000
   ```
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 7. Configure Twilio Webhook

1. In Twilio Console, go to **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
2. Set **WHEN A MESSAGE COMES IN** to: `https://your-ngrok-url.ngrok.io/message`
3. Save the configuration

### 8. Run the Bots

**Terminal 1 - WhatsApp Bot (FastAPI):**
```bash
uvicorn main:app --reload
```

**Terminal 2 - Telegram Bot:**
```bash
python telegram_bot.py
```

Both bots will run simultaneously and share the same inventory data.

### 9. Test the Bots

**WhatsApp:**
- Send a message to your Twilio sandbox number
- Try: "status", "add 2 crates", "subtract 1 crate"

**Telegram:**
- Add bot to a group or message it directly
- Try: "status", "add 2 crates", "subtract 1 crate"
- Or use commands: `/status`, `/commands`

## Usage

### Commands (Work on both WhatsApp and Telegram):

- **Check inventory**: "status", "check inventory", "how many"
- **Add crates**: "add X crates", "add 2 crates"
- **Subtract crates**: "subtract X crates", "remove 1 crate"
- **Help**: "commands", "help"

### Telegram-specific commands:
- `/start` - Welcome message
- `/status` - Check inventory
- `/commands` - List all commands

### Group Chat Benefits (Telegram):
- ✅ Everyone sees updates in real-time
- ✅ Visible history of who did what
- ✅ Better accountability
- ✅ No 72-hour sandbox limit

## Inventory Storage

Inventory is stored in `inventory.json` with the current crate count. The file is automatically created on first run with the default value specified in `.env`.

## Production Deployment

For production use:
1. Deploy the FastAPI app to a hosting service (e.g., Heroku, Railway, AWS)
2. Update the Twilio webhook URL to your production URL
3. Remove the sandbox limitation by completing Twilio's WhatsApp Business API approval process


