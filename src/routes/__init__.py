import os
from fastapi import Request, APIRouter
from fastapi.logger import logger
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from src.services.ai_responses import get_ai_response


whatsapp = APIRouter(
    prefix="/v1"
)

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)
first_message = '''
    Good day, I am Nick the SRSsolar assistant, I can help you with the following:
    
    *Select a solar or backup solution*
    *Pricing of solar and back up solutions*
    *Get someone to call you back*
    
    Feel free to ask me a question as I am trained to answer frequently asked questions.
'''


# Define a route for handling incoming WhatsApp messages
@whatsapp.post('/whatsapp')
async def whatsapp_endpoint(request: Request):
    """
    :param request: Request object from Twilio
    :return: Message acknowledgement with status 200
    """

    logger.info(f"Received request")
    try:
        form = await request.form()
        user_message = form['Body'].lower()  # User's message
        user_number = form['Author']  # User's phone number

        if user_message == "join scared-actually":
            ai_response = first_message
        else:
            # Use OpenAI API for general queries
            ai_response = get_ai_response(user_phone=user_number, message=user_message)

        # Create Twilio WhatsApp response
        client.conversations.v1.conversations(
            form['ConversationSid']
        ).messages.create(body=ai_response)

        return MessagingResponse()
    except Exception as e:
        logger.error(f"Got an exception - {e}")
