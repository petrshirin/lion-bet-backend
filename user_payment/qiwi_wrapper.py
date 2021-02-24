import requests
import string
import random
import urllib
from django.conf import settings
from .models import UserMoneyRequest
from datetime import datetime, timedelta


QIWI_PUBLIC_KEY = settings.QIWI_PUBLIC_KEY
QIWI_SECRET_KEY = settings.QIWI_SECRET_KEY


class QiwiWrapper(object):

    def __init__(self):
        self.url = "https://oplata.qiwi.com/create?"
        self.public_key = QIWI_PUBLIC_KEY
        self.build = ''
        self._generate_build()

    def _generate_build(self):
        self.build = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(32)])

    def create_form(self, amount: float):
        data_time = datetime.now() + timedelta(hours=1)
        data = {
            "publicKey": self.public_key,
            "billId": self.build,
            "amount": amount,
            "comment": self.build,
            'lifetime': data_time.strftime("%Y-%m-%dT%H%M")
        }
        return self.url + urllib.parse.urlencode(data)


def check_payment(payment_request: UserMoneyRequest) -> str:

    if payment_request.accepted is not None:
        return "PAID"

    url = f'https://api.qiwi.com/partner/bill/v1/bills/{payment_request.build}'

    response = requests.get(url, headers={
        "Authorization": f"Bearer {QIWI_SECRET_KEY}"})

    if response.ok:
        data = response.json()
        if data['status']['value'] == 'WAITING':
            return "WAITING"
        elif data['status']['value'] == 'PAID':
            if payment_request.amount < data['amount']['value']:
                return "FAIL, NEED ADMIN"
            payment_request.accepted = True
            payment_request.save()
        elif data['status']['value'] == 'REJECTED':
            payment_request.accepted = False
            payment_request.save()
        elif data['status']['value'] == 'EXPIRED':
            payment_request.accepted = False
            payment_request.save()
        else:
            return data
        return data.get('status')
    else:
        return response.text




