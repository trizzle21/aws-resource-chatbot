import logging
import re
from typing import Dict, List, Tuple, Optional

import boto3

from app.handlers.resource_handler import ResourceHandler
from app.handlers.sqs.sqs_attribute_handler import SQSAttributeHandler
from app import cache

LOG = logging.getLogger(__name__)

"""
TODO: see if I can use nltk tokenize
https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
"""


class SQSHandler(ResourceHandler):
    cache_key = 'sqs_queues'
    queue_url_regex = r'https:\/\/.+[1-9]\/(.+)' 
    intents = {
        'size': SQSAttributeHandler('ApproximateNumberOfMessages'),
        'created': SQSAttributeHandler('CreatedTimestamp'),
        'retention': SQSAttributeHandler('MessageRetentionPeriod')
    }

    def __init__(self, boto3, cache):
        self.client = boto3.client('sqs')

    def handle(self, tokenized_message: List[str], *args, **kwargs) -> str:
        name, url = self.get_name(tokenized_message)
        if not name:
            return 'The SQS Queue you requested does not exist'
        message_intent = self.get_intent(tokenized_message)
        if not message_intent:
            queue_commands = ', '.join(intents.keys())
            return f'The Available Commands for queues are {queue_commands}'

        handler = intents[message_intent]
        value = handler.handle(self.client, url)
        return handler.handle_response(name, value)

    def get_intent(tokenized_message)-> str:
        intent_tokens: List[str] = set(self.intents.keys())
        message_intent = list(intent_tokens.intersection(tokenized_message))
        if message_intent != 1:
            return None
        return message_intent

    def get_name(tokenized_message) -> Optional[Tuple[str, str]]:
        """
            {
                'QueueUrls': [
                    'https://sqs.us-east-2.amazonaws.com/838802343873/test-queue-monitor',
                ]
            }
        """
        queue_names: Dict[str, str]
        if cache.get(self.cache_key):
            queues = cache.get(self.cache_key)
        else:
            queues = self._refresh_queue_names()

        intended_queues: List = list(queue_names.intersection(tokenized_message))
        if len(intended_queues) != 1:
            return None
        queue_name = intended_queues[0]
        return queue_name, queues[queue_name]

    def _refresh_queue_names(self):
        response: Dict[str, str] = self.client.list_queues()
        queues = {re.match(self.queue_url_regex, url).group(1): url for url in response['QueueUrls']}
        cache.set(self.cache_key, queue_names, ex=3600)
        return queues
