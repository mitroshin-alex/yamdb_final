from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, EmailConfirmationViewSet,
    GenreViewSet, ObtainTokenView, ProfileViewSet,
    ReviewViewSet, TitlesViewSet, UserViewSet
)

router_v1 = DefaultRouter()

router_v1.register('auth/signup', EmailConfirmationViewSet, basename='signup')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/token/', ObtainTokenView.as_view(), name='token'),
    path(
        'v1/users/me/',
        ProfileViewSet.as_view({"patch": "partial_update", "get": "retrieve"}),
        name="profile-retrieve-update",
    ),
    path('v1/', include(router_v1.urls)),
]
