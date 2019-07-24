from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Collection

register = template.Library()


@register.simple_tag(takes_context=True)
def get_collect_status(context, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    collector = context['user']
    try:
        collection = Collection.objects.filter(content_type=content_type, object_id=object_id, collector=collector)
    except:
        return None
    else:
        if collection.exists():
            return 'collected'


@register.simple_tag()
def get_collect_total(content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    total = Collection.objects.filter(content_type=content_type, object_id=object_id)
    if total.exists():
        return total.count()
    else:
        return 0
