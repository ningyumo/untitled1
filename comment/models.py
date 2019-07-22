from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User


# 评论
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(max_length=300)

    # 父评论,对哪条评论回复，就是父评论，如果自己是父评论，则该值为Null
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='child_comment', blank=True, null=True)
    # 顶级评论，
    top_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='descendants', blank=True, null=True)

    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']