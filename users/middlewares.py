from django.http import HttpRequest
from .models import AdminPaymentLog, User, Client
import logging


LOG = logging.getLogger(__name__)


class AdminPaymentLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):

        if request.user.is_staff \
                and request.method == 'POST' \
                and 'customeraccount' in request.path \
                and 'change' in request.path:
            user = User.objects.filter(pk=request.POST['user']).first()
            if user:
                old_balance = user.customeraccount.current_balance
            else:
                old_balance = None

        response = self.get_response(request)

        if request.user.is_staff \
                and request.method == 'POST' \
                and 'customeraccount' in request.path \
                    and 'change' in request.path:
            try:
                if not old_balance:
                    return response
                AdminPaymentLog.objects.create(admin=request.user,
                                               amount=abs(float(request.POST['current_balance'])-float(old_balance)))
            except Exception as err:
                LOG.error(err)
        return response

