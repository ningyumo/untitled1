from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Like

register = template.Library()


# 点赞状态，针对任何模型
@register.simple_tag(takes_context=True, name='get_like_status')
def get_like_status(context, content_type, object_id):
    user = context['user']
    content_type = ContentType.objects.get(model=content_type)
    like = Like.objects.filter(content_type=content_type, object_id=object_id, liker=user)
    if like.exists():
        return 'like_like'
    else:
        return 'like_dislike'


# 点赞状态，针对博客
@register.simple_tag(takes_context=True, name='get_like_blog_status')
def get_like_blog_status(context, object_id):
    user = context['user']
    content_type = ContentType.objects.get(model='blog')
    like = Like.objects.filter(content_type=content_type, object_id=object_id, liker=user)
    if like.exists():
        return 'like_blog'
    return None

# 点赞总数，针对任何模型
@register.simple_tag()
def get_like_total(content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    total = Like.objects.filter(content_type=content_type, object_id=object_id)
    if total.exists():
        return total.count()
    else:
        return 0

