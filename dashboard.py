"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'lion_bet_backend.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'lion_bet_backend.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from users.models import Client, AdminPaymentLog
from user_payment.models import UserMoneyRequest
from datetime import datetime, timedelta
from qsstats import QuerySetStats
from django.db.models import QuerySet
from django.utils.timezone import now
from django.db.models import Sum


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for lion_bet_backend.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # Users block
        self.children.append(modules.Group(
            title='Пользователи',
            display='tabs',
            children=[
                UserStatApp(title=u'Статистика'),
                TableStatApp(title='Метрики', stat_name='Пользователей', model='Client'),
                modules.ModelList(
                    _('Данные'),
                    models=(
                        'django.contrib.auth.admin.User',
                        'users.models.Client',
                        'users.models.CustomerAccount',
                        'rest_framework.authtoken.models.Token',
                    )
                ),
                modules.ModelList(
                    _('Ставки'),
                    models=(
                        'user_bet.models.UserBet',
                    )
                ),
                modules.ModelList(
                    _('Обращения'),
                    models=(
                        'techsupport.models.ClientRequest',
                    )
                )

            ]
        ))

        self.children.append(modules.Group(
            title='Ввод/Вывод средств',
            display='tabs',
            children=[
                UserPaymentApp(title=u'Статистика'),
                TableStatApp(title='Метрики', stat_name='Пополнений', model='UserMoneyRequest'),
                modules.ModelList(
                    _('Все запросы'),
                    models=(
                        'user_payment.models.UserMoneyRequest',
                    )
                )

            ]
        ))

        # append a recent actions module
        self.children.append(modules.ModelList(
                    _('Данные о матчах'),
                    models=(
                        'sport_events.models.*',
                    )
                ))

        self.children.append(modules.Group(
            title='Действия Администраторов',
            display='tabs',
            children=[
                AdminPaymentActionsApp(title=u'Логи пополнений'),
                modules.RecentActions(_('Последние действия'), 10)
            ]
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for lion_bet_backend.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)


class UserStatApp(modules.DashboardModule):

    def is_empty(self):
        return self.values == []

    def __init__(self, **kwargs):
        super(UserStatApp, self).__init__(**kwargs)
        self.template = 'graphics.html'
        qs = Client.objects.filter()
        end = now()
        start = end - timedelta(days=30)

        # готовим данные для графика

        data = QuerySetStats(qs, 'date_register').time_series(start, end)
        self.values = [t[1] for t in data]
        self.captions = [t[0].day for t in data]


class UserPaymentApp(modules.DashboardModule):

    def is_empty(self):
        return self.values == []

    def __init__(self, **kwargs):
        super(UserPaymentApp, self).__init__(**kwargs)
        self.template = 'graphics.html'
        qs = UserMoneyRequest.objects.filter(accepted=True, request_type='input')
        end = now()
        start = end - timedelta(days=30)

        # готовим данные для графика
        qss = QuerySetStats(qs, 'date_created')
        qss.aggregate = Sum('amount')
        data = qss.time_series(start, end)
        self.values = [t[1] for t in data]
        self.captions = [t[0].day for t in data]


class AdminPaymentActionsApp(modules.DashboardModule):
    def is_empty(self):
        return False

    def __init__(self, **kwargs):
        super(AdminPaymentActionsApp, self).__init__(**kwargs)
        self.template = 'payment_log.html'
        self.logs = AdminPaymentLog.objects.all()


class TableStatApp(modules.DashboardModule):

    def is_empty(self):
        return False

    def __init__(self, **kwargs):
        super(TableStatApp, self).__init__(**kwargs)
        self.template = 'table_stats.html'
        self.stat_name = kwargs['stat_name']
        if kwargs['model'] == 'Client':
            self.per_day = Client.objects.filter(date_register__gte=now() - timedelta(hours=24)).count()
            self.per_week = Client.objects.filter(date_register__gte=now() - timedelta(days=7)).count()
            self.per_mouth = Client.objects.filter(date_register__gte=now() - timedelta(days=30)).count()
            self.per_all = Client.objects.filter().count()
        elif kwargs['model'] == 'UserMoneyRequest':
            self.per_day = UserMoneyRequest.objects.filter(accepted=True, request_type='input', date_created=now() - timedelta(hours=24)).all().aggregate(Sum('amount'))['amount__sum'] or 0
            self.per_week = UserMoneyRequest.objects.filter(accepted=True, request_type='input', date_created=now() - timedelta(days=7)).all().aggregate(Sum('amount'))['amount__sum'] or 0
            self.per_mouth = UserMoneyRequest.objects.filter(accepted=True, request_type='input', date_created=now() - timedelta(days=30)).all().aggregate(Sum('amount'))['amount__sum'] or 0
            self.per_all = UserMoneyRequest.objects.filter(accepted=True,  request_type='input').all().aggregate(Sum('amount'))['amount__sum'] or 0
