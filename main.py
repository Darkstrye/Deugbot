from fastapi import FastAPI, Request, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
from commands import handle_message

load_dotenv()

app = FastAPI()

# Twilio credentials
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Initialize Twilio client
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN) if ACCOUNT_SID and AUTH_TOKEN else None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "WhatsApp Beer Inventory Bot is running"}


@app.post("/message")
async def receive_message(request: Request):
    """
    Webhook endpoint to receive WhatsApp messages from Twilio.
    """
    try:
        print("=" * 50)
        print("Received webhook request from Twilio")
        print(f"Headers: {dict(request.headers)}")
        
        # Parse form data from Twilio
        form_data = await request.form()
        print(f"Form data: {dict(form_data)}")
        
        incoming_message = form_data.get("Body", "").strip()
        from_number = form_data.get("From", "")
        
        print(f"Message: {incoming_message}")
        print(f"From: {from_number}")
        
        # Process the command
        response_text = handle_message(incoming_message)
        print(f"Response: {response_text}")
        
        # Create TwiML response
        resp = MessagingResponse()
        resp.message(response_text)
        
        print("=" * 50)
        
        # Return TwiML response with correct content type
        return Response(content=str(resp), media_type="application/xml")
    except Exception as e:
        # Log error and return a simple error message
        import traceback
        print(f"Error processing message: {str(e)}")
        print(traceback.format_exc())
        resp = MessagingResponse()
        resp.message("Sorry, there was an error processing your request.")
        return Response(content=str(resp), media_type="application/xml")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "twilio_configured": twilio_client is not None
    }

