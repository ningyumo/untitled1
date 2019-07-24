from django.template import Library
from ..forms import LoginForm

register = Library()


@register.simple_tag()
def get_login_form():
    form = LoginForm()
    return form