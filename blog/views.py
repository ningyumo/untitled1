from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Blog, BlogTag


# 博客列表
class BlogListView(ListView):
    model = Blog
    context_object_name = 'blog_list'
    paginate_by = 10
    paginate_orphans = 5
    template_name = 'blog/blog_list.html'
    page_kwarg = 'page'
    blog_tags_model = BlogTag

    def get_blog_tags(self):
        blog_tags = self.blog_tags_model.objects.all()
        return blog_tags

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogListView, self).get_context_data()
        context['blog_tags'] = self.get_blog_tags()
        return context


blog_list = BlogListView.as_view()


# 带标签的博客列表
class BlogListWithTypeView(BlogListView):
    template_name = 'blog/blog_list_with_tag.html'
    context_object_name = 'blog_list'
    paginate_by = 10
    paginate_orphans = 5
    page_kwarg = 'page'
    blog_tags_model = BlogTag
    tag_kwargs = 'tag'

    def get_queryset(self, **kwargs):
        tag_pk = self.kwargs.get(self.tag_kwargs, None)
        return Blog.objects.filter(tags__pk=tag_pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogListWithTypeView, self).get_context_data(object_list=None, **kwargs)
        context['tag'] = int(self.kwargs.get(self.tag_kwargs, None))
        return context


blog_list_with_type = BlogListWithTypeView.as_view()


# 博客详情
class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        return context


blog_detail = BlogDetailView.as_view()

























