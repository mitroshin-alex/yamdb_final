import django_filters as filters_dj

from reviews.models import Title


class TitleFilter(filters_dj.FilterSet):
    """Title filters"""
    name = filters_dj.CharFilter(
        field_name='name', lookup_expr='contains')
    category = filters_dj.CharFilter(
        field_name='category__slug', lookup_expr='exact')
    genre = filters_dj.CharFilter(
        field_name='genre__slug', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
