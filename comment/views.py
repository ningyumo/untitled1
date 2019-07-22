from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import FormView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse_lazy
from .forms import CommentForm
from .models import Comment


# 提交评论
@method_decorator(login_required, name='dispatch')
class CommentFormView(FormView):
    form_class = CommentForm
    success_url = None
    template_name = None
    data = {}

    def form_valid(self, form):
        object_class = form.cleaned_data['object_class']
        object_id = form.cleaned_data['object_id']
        content = form.cleaned_data['content']
        parent_comment_pk = form.cleaned_data['parent_comment_pk']
        top_comment_pk = form.cleaned_data['top_comment_pk']
        status = form.cleaned_data['status']
        content_type = ContentType.objects.get(model=object_class)

        if parent_comment_pk == '' and top_comment_pk == '':
            comment = Comment.objects.create(content_type=content_type,
                                             object_id=object_id,
                                             content=content,
                                             creater=self.request.user)
            self.data['comment_top_comment_pk'] = ''
        else:
            parent_comment = Comment.objects.get(pk=parent_comment_pk)
            top_comment = Comment.objects.get(pk=top_comment_pk)
            content.replace('回复 %s：' % parent_comment.creater.username, '')
            print(content)
            comment = Comment.objects.create(content_type=content_type,
                                             object_id=object_id,
                                             content=content,
                                             parent_comment=parent_comment,
                                             top_comment=top_comment,
                                             creater=self.request.user)
            self.data['comment_parent_creater_username'] = comment.parent_comment.creater.username
            self.data['comment_top_comment_pk'] = comment.top_comment.pk

        self.data['comment_pk'] = comment.pk
        self.data['comment_creater_username'] = comment.creater.username
        self.data['comment_content'] = comment.content
        self.data['create_time'] = comment.create_time.strftime("%Y-%m-%d %H:%M:%S")
        self.data['status'] = status
        return JsonResponse(self.data)

    def form_invalid(self, form):
        status = form.cleaned_data['status']
        self.data['status'] = status
        return JsonResponse(self.data)


comment_submit = CommentFormView.as_view()


# 删除评论
@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    context_object_name = 'comment'
    success_url = reverse_lazy('home')


comment_delete = CommentDeleteView.as_view()
