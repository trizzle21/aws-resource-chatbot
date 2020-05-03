import logging
from typing import List, Optional

import boto3

from app import application as app
from app.resources import message_resources

from app.handlers.resource_handler import ResourceHandler

from app.resources import message_resources
from app.exceptions import AWSMonitorException

LOG = logging.getLogger(__name__)


def get_message_from_resource(resource_handler: Optional[ResourceHandler], tokenized_message: List[str]) -> str:
    if not resource_handler:
        raise AWSMonitorException
    return resource_handler.handle(tokenized_message)


def get_resource(tokenized_message: List['str']) -> ResourceHandler:
    resource_names = set(message_resources.keys())
    desired_resources = list(resource_names.intersection(tokenized_message))
    if len(desired_resources) != 1:
        raise AWSMonitorException
    
    resource = message_resources[desired_resources[0]]
    return resource(boto3, app.cache)


def tokenize_message(message: str) -> List[str]:
    """
    TODO: see if I can use nltk tokenize
    https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
    """
    return list(set(message.split(' ')))
