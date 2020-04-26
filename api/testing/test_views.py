import json
import os
import unittest

# import twilio
from fixtures.twilio_fixture import TwilioTestClient
# # Replace real client with our test client
# twilio.Client = TwilioTestClient

from dotenv import load_dotenv
load_dotenv(verbose=True)

from app import views, application as app
from app.handlers.message_handlers import MessageHandler

# set our application to testing mode
app.testing = True
views.message_handler = MessageHandler(TwilioTestClient(
    os.getenv('TEST_ACCOUNT_SID'), 
    os.getenv('TEST_AUTH_TOKEN')
))


class TestApi(unittest.TestCase):

    def setUp(self):
        pass 

    def test_sqs_message_handler(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            # client.client = TwilioTestClient
            
            sent = {'Body': 'sqs test_sqs_queue'}
            result = client.post(
                '/receive-events',
                data=sent
            )
            # check result from server with expected data
            self.assertTrue(sent['Body'] in str(result.data))

    @staticmethod
    def _create_and_populate_test_queue(queue_name):
        pass
