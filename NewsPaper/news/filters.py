import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    title_field = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    date_field = django_filters.DateFilter(field_name='time_created', lookup_expr='lt')
    author = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains',
                                                       label='Author')

    class Meta:
        model = Post
        fields = []
