import requests
import string
import random
import urllib
from django.conf import settings


QIWI_PUBLIC_KEY = settings.QIWI_PUBLIC_KEY


class QiwiWrapper(object):

    def __init__(self):
        self.url = "https://oplata.qiwi.com/create?"
        self.public_key = QIWI_PUBLIC_KEY
        self.build = ''
        self._generate_build()

    def _generate_build(self):
        self.build = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(32)])

    def create_form(self, amount: float):
        data = {
            "publicKey": self.public_key,
            "build": self.build,
            "amount": amount
        }
        return self.url + urllib.parse.urlencode(data)


