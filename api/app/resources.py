from typing import Dict

from app.handlers.resource_handler import (
    ResourceHandler,
)

from app.handlers.sqs import (
    SQSHandler,
)

from app.handlers.kinesis import (
    KinesisHandler,
)

message_resources: Dict[str, ResourceHandler] = {
    'sqs': SQSHandler,
    'kinesis': KinesisHandler
}
