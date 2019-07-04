from django.shortcuts import render
from django.views.generic.base import TemplateView


# 首页
class Index(TemplateView):
    template_name = 'home.html'

index = Index.as_view()
