import logging
import boto3

from app.handlers.resource_handlers.resource_handler import ResourceHandler

LOG = logging.getLogger(__name__)

class SQSHandler(ResourceHandler):

    def handle(self, name, *args, **kwargs):
        LOG.info(f'handling getting queue size for {name}')
        pass