import logging

from twilio.rest import Client 
from twilio.base.exceptions import TwilioRestException

from app.settings import DEBUG, FROM_PHONE_NUMBER
from app.resources import message_resource_handler

LOG = logging.getLogger(__name__)


class MessageHandler:

    def __init__(self, client):
        self.client = client

    def handle_send_message(self, to, message):
        if not DEBUG and not is_valid_number(to):
            LOG.warning(f'Phone Number is an invalid number')
            return
        message = self.client.messages.create( 
            from_=FROM_PHONE_NUMBER,
            to=to,
            body=message,
        )
        return message.sid

    def is_valid_number(self, number: str) -> bool:
        try:
            response = self.client.lookups.phone_numbers(number).fetch(type="carrier")
            return True
        except TwilioRestException as e:
            if e.code == 20404:
                return False
            else:
                raise e

    @staticmethod
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
