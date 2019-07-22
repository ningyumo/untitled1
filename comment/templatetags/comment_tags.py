from django.template import Library
from comment.forms import CommentForm

register = Library()


@register.simple_tag(name='get_comment_form')
def get_comment_form(obj_class, obj_pk, parent_comment_pk=None, top_comment_pk=None):
    return CommentForm(initial={
        'object_class': obj_class,
        'object_id': obj_pk,
        'parent_comment_pk': parent_comment_pk,
        'top_comment_pk': top_comment_pk,
    })

