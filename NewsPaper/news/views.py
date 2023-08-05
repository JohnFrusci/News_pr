from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import Post
from .filters import PostFilter


class PostsList(ListView):
    paginate_by = 2
    model = Post
    ordering = ['time_created']
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostsSearch(ListView):
    model = Post
    ordering = ['time_created']
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostsDetail(DetailView):
    # model = Post
    template_name = 'post.html'
    queryset = Post.objects.all()
    # context_object_name = 'post'


class PostsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm


class PostsUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
