from django.template import Library
from django.utils import timezone
from comment.forms import CommentForm
from blog.models import Blog
from django.db.models import Count


register = Library()


@register.simple_tag(name='get_comment_form')
def get_comment_form(obj_class, obj_pk, parent_comment_pk=None, top_comment_pk=None):
    return CommentForm(initial={
        'object_class': obj_class,
        'object_id': obj_pk,
        'parent_comment_pk': parent_comment_pk,
        'top_comment_pk': top_comment_pk,
    })


@register.simple_tag()
def get_today_comment_total(blog_pk):
    time = timezone.now()
    total = Blog.objects.filter(pk=blog_pk, comment__create_time__date=time).annotate(comment_total=Count('comment'))[0].comment_total
    return total