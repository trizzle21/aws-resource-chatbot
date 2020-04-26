import logging

from flask import request, jsonify
from twilio.rest import Client 
from twilio.base.exceptions import TwilioRestException

from app import application as app
from app.resources import message_resource_handler
from app.handlers.message_handlers import MessageHandler
from app.settings import (
    DEBUG,
    TEST_PHONE_TO,
    TEST_ACCOUNT_SID,
    TEST_AUTH_TOKEN,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)

from app.resources import message_resource_handler

LOG = logging.getLogger(__name__)

client = Client(TEST_ACCOUNT_SID, TEST_AUTH_TOKEN) 
message_handler = MessageHandler(client)

@app.route('/')
def hello_world():
    return 'Your App is running!'

# {
#     "Body": "modified message text",
#     "Attributes": "{\"key\" : \"value\"}"
# }
@app.route('/receive-events', methods=['POST'])
def receive_events():
    """
        Recieve SMS Events from the Twilio Webhook :)  

    """
    #TODO Make POST endpoint with Twilio body 
    LOG.info('Receiving incoming sms message from')

    webhook_body = request.values
    message_body = webhook_body.get('Body', None)
    if message_body:
        message_sid = message_handler.handle_send_message(TEST_PHONE_TO, message_body)
    return jsonify(**{'body': message_body})


@app.route('/notification-events', methods=['POST'])
def notification_events():
    LOG.info('Receiving incoming webhook message {request.}')
    message_body = "sqs test_sqs_queue"
    message_sid = message_handler.handle_send_message(TEST_PHONE_TO, message_body)
    return message_sid
