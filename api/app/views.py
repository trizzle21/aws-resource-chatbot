import logging
from typing import Set, List, Optional

from flask import request, jsonify
from twilio.rest import Client 
from twilio.base.exceptions import TwilioRestException

from app import application as app
from app.resources import message_resource_handler
from app.handlers import ResourceHandler
from app.handlers.message_handlers import MessageHandler
from app.settings import (
    DEBUG,
    TEST_PHONE_TO,
    TEST_ACCOUNT_SID,
    TEST_AUTH_TOKEN,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)

from app.resources import message_resources

LOG = logging.getLogger(__name__)
DEFAULT_MESSAGE = 'Provided resource not found'

client = Client(TEST_ACCOUNT_SID, TEST_AUTH_TOKEN) 
message_handler = MessageHandler(client)


# TODO remove this endpoint
@app.route('/')
def hello_world():
    return 'Your App is running!'

{
    "Body": "modified message text",
    "Attributes": "{\"key\" : \"value\"}"
}
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

    webhook_body: Dict[str, str] = request.values
    message_body = webhook_body.get('Body', None)
    tokenized_message: Set[str] = _tokenize_message(message_body)
    resource_handler: ResourceHandler = _get_resource(tokenized_message)
    message_response: str = _get_message_from_resource(resource_handler, tokenized_message)    
    
    message_sid = message_handler.handle_send_message(TEST_PHONE_TO, message_response)
    return jsonify(**{'body': message_body})


# TODO: decide if this endpoint is necessary
@app.route('/notification-events', methods=['POST'])
def notification_events():
    LOG.info('Receiving incoming webhook message')
    message_body = "sqs test_sqs_queue"
    message_sid = message_handler.handle_send_message(TEST_PHONE_TO, message_body)
    return message_sid


def _get_message_from_resource(resource_handler: Optional[ResourceHandler], tokenized_message: List[str]) -> str:
    if not resource:
        return DEFAULT_MESSAGE
    return resource.handle(tokenized_message)


def _get_resource(tokenized_message) -> ResourceHandler
    resource_names = set(message_resources.keys())
    desired_resources = resource_names.intersection(tokenized_message)
    if desired_resources != 1:
        return None
    return desired_resources[0]


def _tokenize_message(message):
    """
    TODO: see if I can use nltk tokenize
    https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
    """
    return set(message.split(' '))
