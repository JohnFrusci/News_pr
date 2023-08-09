from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import NewsForm
from .models import Post, Category
from .filters import PostFilter


class PostsList(ListView):
    paginate_by = 2
    model = Post
    ordering = ['time_created']
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
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


class PostsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news_create.html'
    form_class = NewsForm


class PostsUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news_create.html'
    form_class = NewsForm

    # login_url = reverse_lazy('home')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('home')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-time_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

