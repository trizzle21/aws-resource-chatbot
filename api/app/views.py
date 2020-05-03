import logging
from typing import Set, List, Optional
import boto3

from flask import request, jsonify
from twilio.rest import Client 

from app import application as app
from app.exceptions import AWSMonitorException
from app.handlers.resource_handler import ResourceHandler
from app.services.twilio_message_service import TwilioMessageService
from app.settings import (
    DEBUG,
    TEST_PHONE_TO,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)
from app.utils import (
    get_message_from_resource,
    get_resource,
    tokenize_message,
)


LOG = logging.getLogger(__name__)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
message_handler = TwilioMessageService(client)


# TODO remove this endpoint
@app.route('/')
def hello_world():
    return 'Your App is running!'


@app.route('/receive-events', methods=['POST'])
def receive_events():
    """
        Recieve SMS Events from the Twilio Webhook :)  
        TODO: ensure endpoint is only Twilio!

        Expected Json Body
        {
            "Body": "modified message text",
            "Attributes": "{\"key\" : \"value\"}"
        }
    """
    #TODO Make POST endpoint with Twilio body 
    LOG.info('Receiving incoming sms message from')
    #TODO implement STS and user identification via sqlite
    try:
        webhook_body: Dict[str, str] = request.values
        message_body = webhook_body.get('Body', None)
        tokenized_message: List[str] = tokenize_message(message_body)
        resource_handler: ResourceHandler = get_resource(tokenized_message)
        message_response: str = get_message_from_resource(resource_handler, tokenized_message)    
    except AWSMonitorException as err:
        message_response: str = err.message
    message_sid = message_handler.send_message(TEST_PHONE_TO, message_response)
    return jsonify(body=message_response)


# TODO: Move To Adding Slack
@app.route('/slack-events', methods=['POST'])
def notification_events():
    LOG.info('Receiving incoming webhook message')
    message_body = "sqs test_sqs_queue"
    message_sid = message_handler.handle_send_message(TEST_PHONE_TO, message_body)
    return message_sid
