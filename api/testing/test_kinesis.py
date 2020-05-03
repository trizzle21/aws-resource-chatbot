import json, sys
import os
import unittest

# import twilio
from fixtures.twilio_fixture import TwilioTestClient
import boto3
from moto import mock_kinesis

from dotenv import load_dotenv
load_dotenv(verbose=True)


from app import views, application as app
from app.exceptions import AWSResourceMissing, AWSInvalidCommand
from app.handlers.kinesis.kinesis_attribute_handler import KinesisAttributeHandler
from app.handlers.kinesis.kinesis_limit_handler import KinesisLimitHandler

from app.handlers.kinesis.kinesis_handler import KinesisHandler
from app.services.twilio_message_service import TwilioMessageService
from testing.fixtures.cache_fixture import Cache

# set our application to testing mode
app.testing = True
views.message_handler = TwilioMessageService(TwilioTestClient(
    os.getenv('TEST_ACCOUNT_SID'),
    os.getenv('TEST_AUTH_TOKEN')
))


class ReceiveEventKinesisApi(unittest.TestCase):
    stream_name = 'test_kinesis_stream'


    @mock_kinesis
    def test_kinesis_message_handler_with_encryption_type_message_returns_size_metadata(self):
        with app.test_client() as client:
            # Arrange
            client.application.cache = Cache()
            self._create_and_populate_test_stream(self.stream_name, 123)

            sent = {'Body': 'what is the kinesis stream test_kinesis_stream encryption type'}
            expected = KinesisAttributeHandler('EncryptionType').handle_response(self.stream_name, 'None')

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])
            # self._delete_test_stream(self.stream_name)

    @mock_kinesis
    def test_kinesis_message_handler_without_name_returns_resource_message(self):
        with app.test_client() as client:
            # Arrange
            client.application.cache = Cache()
            self._create_and_populate_test_stream(self.stream_name, 123)

            sent = {'Body': 'what is the kinesis stream encryption type'}
            expected = AWSResourceMissing('kinesis').message

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])

    @mock_kinesis
    def test_sqs_message_handler_with_no_kinesis_returns_missing_resource(self):
        with app.test_client() as client:
            # Arrange
            cache = Cache()
            client.application.cache = cache
            Cache.data = {}

            sent = {'Body': 'what is the kinesis stream test_kinesis_stream encryption type'}
            expected = AWSResourceMissing('kinesis').message

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])


    @mock_kinesis
    def test_kinesis_message_handler_with_no_intent_returns_missing_resource(self):
        with app.test_client() as client:
            # Arrange
            client.application.cache = Cache()
            self._create_and_populate_test_stream(self.stream_name, 123)

            sent = {'Body': 'what is the kinesis stream test_kinesis_stream blaaah'}
            expected = AWSInvalidCommand('kinesis', set(KinesisHandler.intents.keys())).message

            # Act
            result = client.post(
                '/receive-events',
                data=sent
            )
            result_payload = result.data.decode("utf-8")

            # assert
            self.assertEqual(expected, json.loads(result_payload)['body'])

    @staticmethod
    def _create_and_populate_test_stream(stream_name, shard_count):
        client = boto3.client('kinesis')
        client.create_stream(
            StreamName=stream_name,
            ShardCount=shard_count
        )


if __name__ == '__main__':
    unittest.main()
