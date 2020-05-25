import json, sys
import os
import unittest

# import twilio
from fixtures.twilio_fixture import TwilioTestClient
import boto3
from moto import mock_sqs
from mock import patch


from dotenv import load_dotenv
load_dotenv(verbose=True)

from app import views, application as app
from app.exceptions import AWSResourceMissing, AWSInvalidCommand
from app.handlers.sqs.sqs_attribute_handler import SQSAttributeHandler
from app.handlers.sqs.sqs_handler import SQSHandler
from app.services.twilio_message_service import TwilioMessageService
from testing.fixtures.cache_fixture import Cache

# set our application to testing mode
app.testing = True
views.message_handler = TwilioMessageService(TwilioTestClient(
    os.getenv('TEST_ACCOUNT_SID'),
    os.getenv('TEST_AUTH_TOKEN')
))


@patch('app.views.db')
@patch('app.views.assumed_role_session')
class ReceiveEventSQSApi(unittest.TestCase):
    test_queue_name = 'test_sqs_queue'
    valid_phone = '+15555555555'

    @mock_sqs
    def test_sqs_message_handler_with_size_message_returns_size_metadata(self, role_service, db):
        db.query_db.return_value = ('test_arn',)
        role_service.return_value = boto3.Session()
        with app.test_client() as client:
            # Arrange
            client.application.cache = Cache()
            self._create_and_populate_test_queue(self.test_queue_name)

            sent = self._create_webhook_payload(self.valid_phone, 'sqs size test_sqs_queue')
            expected = SQSAttributeHandler('ApproximateNumberOfMessages').handle_response(self.test_queue_name, 0)

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])

    @mock_sqs
    def test_sqs_message_handler_without_name_returns_resource_message(self, role_service, db):
        db.query_db.return_value = ('test_arn',)
        role_service.return_value = boto3.Session()
        with app.test_client() as client:
            # Arrange
            client.application.cache = Cache()
            self._create_and_populate_test_queue(self.test_queue_name)
            
            sent = self._create_webhook_payload(self.valid_phone, 'sqs size')
            expected = AWSResourceMissing('sqs').message

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])

    @mock_sqs
    def test_sqs_message_handler_with_no_queue_returns_missing_resource(self, role_service, db):
        db.query_db.return_value = ('test_arn',)
        role_service.return_value = boto3.Session()

        with app.test_client() as client:
            # Arrange
            client.application.cache = Cache()

            sent = self._create_webhook_payload(self.valid_phone, 'sqs size')
            expected = AWSResourceMissing('sqs').message

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])


    @mock_sqs
    def test_sqs_message_handler_with_no_intent_returns_missing_resource(self, role_service, db):
        db.query_db.return_value = ('test_arn',)
        role_service.return_value = boto3.Session()
        with app.test_client() as client:
            # Arrange
            client.application.cache = Cache()
            self._create_and_populate_test_queue(self.test_queue_name)
            sent = self._create_webhook_payload(self.valid_phone, 'sqs test_sqs_queue')
            expected = AWSInvalidCommand('sqs', set(SQSHandler.intents.keys())).message

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])

    @staticmethod
    def _create_and_populate_test_queue(queue_name):
        client = boto3.client('sqs')
        client.create_queue(QueueName=queue_name)

    @staticmethod
    def _create_webhook_payload(phone, message):
        return {         
            'From': phone,
            'Body': message
        }
