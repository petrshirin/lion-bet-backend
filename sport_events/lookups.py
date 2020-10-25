from ajax_select import register, LookupChannel
from .models import MatchEvent
from ajax_select.lookup_channel import LookupChannel
from django.contrib.contenttypes.models import ContentType


@register('ajax_events')
class TagsLookup(LookupChannel):

    model = MatchEvent

    def get_query(self, q, request):
        return self.model.objects.filter(oc_group_name__startswith=q)[:10]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % str(item)

    def can_add(self, user, other_model):
        return True
