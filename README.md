# WhatsApp Beer Inventory Bot

A simple WhatsApp bot for managing beer crate inventory for a student bar. Built with Twilio WhatsApp API and FastAPI.

## Features

- Check current inventory via WhatsApp
- Subtract beers from inventory when added to fridge
- Simple JSON-based storage (no database needed)
- Crate-based inventory management

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

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Twilio credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   DEFAULT_CRATES=50
   ```

### 5. Expose Local Server (for Development)

1. Install ngrok: https://ngrok.com/download
2. Start the FastAPI server (see next step)
3. In a new terminal, run:
   ```bash
   ngrok http 8000
   ```
4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 6. Configure Twilio Webhook

1. In Twilio Console, go to **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
2. Set **WHEN A MESSAGE COMES IN** to: `https://your-ngrok-url.ngrok.io/message`
3. Save the configuration

### 7. Run the Application

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

### 8. Test the Bot

1. Send a WhatsApp message to your Twilio sandbox number
2. Try commands like:
   - "check inventory"
   - "how many beers"
   - "added 4 beers"
   - "add 10 beers"

## Usage

Send WhatsApp messages to the bot with natural language commands:

- **Check inventory**: "check inventory", "how many beers", "inventory"
- **Subtract beers**: "added 4 beers", "add 10 beers", "added 2 beers to fridge"

## Inventory Storage

Inventory is stored in `inventory.json` with the current crate count. The file is automatically created on first run with the default value specified in `.env`.

## Production Deployment

For production use:
1. Deploy the FastAPI app to a hosting service (e.g., Heroku, Railway, AWS)
2. Update the Twilio webhook URL to your production URL
3. Remove the sandbox limitation by completing Twilio's WhatsApp Business API approval process


