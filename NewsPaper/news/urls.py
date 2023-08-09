from django.urls import path
from .models import *
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='home'),
    path('<int:pk>', PostsDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='search'),
    path('add/', PostsCreateView.as_view(), name='post_create'),
    path('edit/<int:pk>', PostsUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostsDeleteView.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]
