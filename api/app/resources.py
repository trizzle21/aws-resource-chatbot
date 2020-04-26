from app.handlers.resource_handlers import (
    SQSHandler,
)

message_resource_handler = {
    'sqs': SQSHandler,
}