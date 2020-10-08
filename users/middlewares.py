from django.http import HttpRequest
from .models import AdminPaymentLog, User, Client
import logging


LOG = logging.getLogger(__name__)


class AdminPaymentLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):

        user = User.objects.get(pk=request.POST['user'])
        old_balance = user.customeraccount.current_balance

        response = self.get_response(request)

        if request.user.is_staff \
                and request.method == 'POST' \
                and 'customeraccount' in request.path \
                and 'change' in request.path:
            try:

                AdminPaymentLog.objects.create(admin=request.user,
                                               amount=abs(float(request.POST['current_balance'])-float(old_balance)))
            except Exception as err:
                LOG.error(err)
        return response

