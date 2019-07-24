from django.views.generic.base import TemplateView
from django.utils import timezone
from django.db.models import Count
from blog.models import Blog


# 首页
class Index(TemplateView):
    template_name = 'home.html'

    # 最新发布
    def get_new(self):
        new_blog_list = Blog.objects.all().order_by('-created_time')[:5]
        return new_blog_list

    # 最多评论
    def get_most_comment_blogs(self):
        most_comment_blogs = Blog.objects.all().annotate(comment_total=Count('comment')).order_by('-comment_total')[:5]
        return most_comment_blogs

    # 最多点赞
    def get_most_like_blog(self):
        most_like_blogs = Blog.objects.all().annotate(like_total=Count('like')).order_by('-like_total')[:5]
        return most_like_blogs

    # 今日热门
    # def get_today_comment_blog(self):
    #     time = timezone.now()
    #     today_comment_blogs = Blog.objects.filter(comment__create_time__date=time).annotate(comment_total=Count('comment')).order_by('-comment_total')
    #     return today_comment_blogs
    # 今日好评

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['new_blog_list'] = self.get_new()
        context['most_comment_blogs'] = self.get_most_comment_blogs()
        context['most_like_blogs'] = self.get_most_like_blog()
        # context['today_comment_blogs'] = self.get_today_comment_blog()
        return context


index = Index.as_view()


