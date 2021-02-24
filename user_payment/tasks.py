from lion_bet_backend.celery import app
from .qiwi_wrapper import check_payment
from .models import UserMoneyRequest
from datetime import timedelta
from django.utils.timezone import now
import logging

LOG = logging.getLogger(__name__)


@app.task
def update_user_input_payments_requests():
    user_payments = UserMoneyRequest.objects.filter(request_type='input', accepted=None).all()
    for user_payment in user_payments:
        try:
            result = check_payment(user_payment)
            LOG.error(f'{user_payment.build} {result}')
        except Exception as e:
            LOG.error(e)

