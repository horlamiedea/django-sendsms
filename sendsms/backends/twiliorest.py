#-*- coding: utf-8 -*-

"""
this backend requires the twilio python library: http://pypi.python.org/pypi/twilio/
"""
try:
    from twilio.rest import TwilioRestClient
except ImportError:
    from twilio.rest import Client as TwilioRestClient

from django.conf import settings
from sendsms.backends.base import BaseSmsBackend

TWILIO_ACCOUNT_SID = getattr(settings, 'SENDSMS_TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = getattr(settings, 'SENDSMS_TWILIO_AUTH_TOKEN', '')


class SmsBackend(BaseSmsBackend):
    def send_messages(self, messages):
        client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for message in messages:
            for to in message.to:
                try:
                    client.messages.create(
                        to=to,
                        from_=message.from_phone,
                        body=message.body
                    )
                except Exception as e:
                    if not self.fail_silently:
                        raise Exception("Error: " + str(e))
