from django.contrib.contenttypes.models import ContentType
from django import  forms
from .models import Comment

# 提交评论表单
class CommentForm(forms.Form):
    object_class = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.CharField(widget=forms.HiddenInput())

    content = forms.CharField(widget=forms.Textarea(attrs={
                                'class': 'form-control'
                            }))
    parent_comment_pk = forms.CharField(required=False, widget=forms.HiddenInput())
    top_comment_pk = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content.strip()) == 0:
            raise forms.ValidationError('输入内容不能为空')
        return content

    def clean(self):
        object_class = self.cleaned_data['object_class']
        object_id = self.cleaned_data['object_id']
        content = self.cleaned_data['content']
        parent_comment_pk = self.cleaned_data['parent_comment_pk']
        top_comment_pk = self.cleaned_data['top_comment_pk']
        # 验证评论内容
        if len(content.strip()) == 0:
            self.cleaned_data['status'] = 'CONTENT_ERRORS'
            raise forms.ValidationError('输入内容不能为空')
        # 验证评论对象是否存在
        content_type = ContentType.objects.get(model=object_class)
        model = content_type.model_class()
        if not model.objects.filter(pk=object_id).exists():
            self.cleaned_data['status'] = 'COMMENT_OBJECT_ERRORS'
            raise forms.ValidationError('评论对象不存在')

        self.cleaned_data['status'] = 'SUCCESS'
        return self.cleaned_data
