import logging
from typing import Set, List, Optional
import boto3

from flask import request, jsonify
from twilio.rest import Client 
from twilio.base.exceptions import TwilioRestException

from app import application as app
from app.resources import message_resources

from app.handlers.resource_handler import ResourceHandler
from app.services.twilio_message_service import TwilioMessageService

from app.settings import (
    DEBUG,
    TEST_PHONE_TO,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)

from app.resources import message_resources
from app.exceptions import AWSMonitorException, AWSResourceMissing

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
    try:
        webhook_body: Dict[str, str] = request.values
        message_body = webhook_body.get('Body', None)
        tokenized_message: List[str] = _tokenize_message(message_body)
        resource_handler: ResourceHandler = _get_resource(tokenized_message)
        message_response: str = _get_message_from_resource(resource_handler, tokenized_message)    
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


def _get_message_from_resource(resource_handler: Optional[ResourceHandler], tokenized_message: List[str]) -> str:
    if not resource_handler:
        raise AWSMonitorException
    return resource_handler.handle(tokenized_message)


def _get_resource(tokenized_message) -> ResourceHandler:
    resource_names = set(message_resources.keys())
    desired_resources = list(resource_names.intersection(tokenized_message))
    if len(desired_resources) != 1:
        raise AWSMonitorException
    
    resource = message_resources[desired_resources[0]]
    return resource(boto3, app.cache)


def _tokenize_message(message) -> List[str]:
    """
    TODO: see if I can use nltk tokenize
    https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
    """
    return list(set(message.split(' ')))
