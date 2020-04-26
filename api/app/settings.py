import os

DEBUG = bool(os.getenv("DEBUG"))
TESTING = bool(os.getenv("TESTING"))
PORT = int(os.getenv("PORT"))
TWILIO_ACCOUNT_ID = os.getenv("TWILIO_ACCOUNT_ID")

TEST_PHONE = '+15005550006'
TEST_PHONE_TO = os.getenv("TEST_PHONE_TO")
PHONE_NUMBER = TEST_PHONE if DEBUG else os.getenv("PHONE_NUMBER")
PHONE_NUMBER_SID = os.getenv("PHONE_NUMBER_SID")


# Relevant for Sending
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TEST_ACCOUNT_SID = os.getenv("TEST_ACCOUNT_SID")
TEST_AUTH_TOKEN = os.getenv("TEST_AUTH_TOKEN")

print(os.environ)
