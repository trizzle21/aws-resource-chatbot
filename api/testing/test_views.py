import json, sys
import os
import unittest

# import twilio
from fixtures.twilio_fixture import TwilioTestClient
from moto import mock_sqs
# # Replace real client with our test client
# twilio.Client = TwilioTestClient

from dotenv import load_dotenv
load_dotenv(verbose=True)

from app import views, application as app
from app.handlers.message_handler import TwilioMessageService

# set our application to testing mode
app.testing = True
views.message_handler = TwilioMessageService(TwilioTestClient(
    os.getenv('TEST_ACCOUNT_SID'), 
    os.getenv('TEST_AUTH_TOKEN')
))


class TestApi(unittest.TestCase):

    def setUp(self):
        pass 

    @mock_sqs
    def test_sqs_message_handler(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            # client.client = TwilioTestClient
            
            sent = {'Body': 'sqs tets_sqs_queue'}
            result = client.post(
                '/receive-events',
                data=sent
            )
            # check result from server with expected data
            self.assertTrue(sent['Body'] in str(result.data))

    @staticmethod
    def _create_and_populate_test_queue(queue_name):
        pass


if __name__ == '__main__':
    unittest.main()
