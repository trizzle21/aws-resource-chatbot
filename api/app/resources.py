from typing import Dict

from app.handlers.resource_handler import (
    ResourceHandler,
)

from app.handlers.sqs import (
    SQSHandler,
)


message_resources: Dict[str, ResourceHandler] = {
    'sqs': SQSHandler,
}
