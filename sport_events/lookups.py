from ajax_select import register, LookupChannel
from .models import MatchEvent, Match
from ajax_select.lookup_channel import LookupChannel
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import Q
import logging


LOG = logging.getLogger(__name__)


@register('ajax_events')
class EventManyLookup(LookupChannel):

    model = MatchEvent

    def get_query(self, q, request):
        return self.model.objects.filter(oc_group_name__startswith=q)[:10]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % str(item)

    def can_add(self, user, other_model):
        return True


@register('ajax_match_select')
class MatchLookup(LookupChannel):

    model = Match

    def get_query(self, q, request):
        LOG.error(q)
        try:
            return self.model.objects.filter(Q(game_num=int(q)))
        except Exception as e:
            pass
        LOG.error(self.model.objects.filter(Q(name__contains=q) | Q(opp_1_name__contains=q) | Q(opp_2_name__contains=q)).order_by('admin_created').all())
        return self.model.objects.filter(Q(name__contains=q) | Q(opp_1_name__contains=q) | Q(opp_2_name__contains=q)).order_by('admin_created')

    def can_add(self, user, other_model):
        return True
