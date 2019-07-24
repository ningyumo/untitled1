from django.views.generic.base import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Collection


# 收藏
class CollectView(TemplateView):
    template_name = None
    data = {}

    def get_context_data(self, **kwargs):
        print(11111)
        if self.request.user.is_authenticated:
            print(2222)
            content_type = self.request.GET.get('content_type')
            object_id = self.request.GET.get('object_id')
            content_type = ContentType.objects.get(model=content_type)
            colletion, created = Collection.objects.get_or_create(collector=collector, content_type=content_type, object_id=object_id)
            if created:
                self.data['status'] = 'CREATE_SUCCESS'
            else:
                colletion.delete()
                self.data['status'] = 'DELETE_SUCCESS'
        else:
            print(333330)
            self.data['status'] = 'NO_LOGIN_ERRORS'
        return self.data

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_context_data(**kwargs))


collect = CollectView.as_view()