from app.handlers.resource_handlers import (
    SQSHandler,
    ResourceHandler,
)

message_resources: Dict[str, ResourceHandler] = {
    'sqs': SQSHandler,
}
