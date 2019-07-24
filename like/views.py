from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Like


# 改变点赞状态
# @method_decorator(login_required, name='dispatch')
class LikeChangeView(TemplateView):
    template_name = None
    context = {}

    def get_context_data(self, **kwargs):
        model = self.request.GET.get('content_type')
        content_type = ContentType.objects.get(model=model)
        object_id = self.request.GET.get('object_id')
        if self.request.user.is_authenticated:
            like, created = Like.objects.get_or_create(content_type=content_type, object_id=object_id, liker=self.request.user)
            if created:
                self.context['status'] = 'CREATED_SUCCESS'
            else:
                like.delete()
                self.context['status'] = 'DELETE_SUCCESS'
        else:
            self.context['status'] = 'NO_LOGIN_ERROR'
        return self.context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return JsonResponse(context)


like_change = LikeChangeView.as_view()