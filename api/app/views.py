import logging

from app import application as app
from app.handlers.message_handlers import handle_send_message
from app.settings import TEST_PHONE_TO

LOG = logging.getLogger(__name__)

@app.route('/')
def hello_world():
    return 'Your App is running!'


@app.route('/receive-events')
def receive_events():
    #TODO Make POST endpoint with Twilio body 
    LOG.info('Receiving incoming sms message from')

    #TODO Add Resource handler and resource decision maker 
    message_body = "testing"
    message_sid = handle_send_message(to, message_body)
    return message_sid


@app.route('/notification-events')
def receive_events():
    LOG.info('Receiving incoming webhook message')
    message_body = "testing"
    message_sid = handle_send_message(TEST_PHONE_TO, message_body)
    return message_sid
