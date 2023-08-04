from django.urls import path
from .models import *
from .views import *

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostsDetail.as_view()),
    path('search/', PostsSearch.as_view())
]