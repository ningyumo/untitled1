from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Collection

register = template.Library()


@register.simple_tag(takes_context=True)
def get_collect_status(context, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    collector = context['user']
    collection = Collection.objects.filter(content_type=content_type, object_id=object_id, collector=collector)
    if collection.exists():
        return 'collected'
