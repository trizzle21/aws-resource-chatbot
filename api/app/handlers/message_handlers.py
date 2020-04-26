import logging

from twilio.rest import Client 
from twilio.base.exceptions import TwilioRestException

from app.settings import (
    DEBUG,
    PHONE_NUMBER,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TEST_ACCOUNT_SID,
    TEST_AUTH_TOKEN,
)
from app.resources import message_resource_handler

LOG = logging.getLogger(__name__)

client = Client(TEST_ACCOUNT_SID, TEST_AUTH_TOKEN) 


def is_valid_number(number: str) -> bool:
    try:
        response = client.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e

def message_intent_parser(message):
    """
        Expecting messages in the format "sqs example-resource-name"
    """
    values = message.split(' ')
    if values[0] not in message_resource_handler.keys():
        return
    resource = values[0]
    resource_name = values[1]
    return values[0], values[1]


def handle_send_message(to, message):
    if not DEBUG and not is_valid_number(to):
        LOG.warning(f'Phone Number is an invalid number')
        return
    message = client.messages.create( 
        from_=PHONE_NUMBER,
        to=to,
        body=message,
    )
    return message.sid
