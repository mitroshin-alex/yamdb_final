from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import (CreateListDestroyViewSet, CreateViewSet,
                     RetrievePatchViewSet)
from .permissions import (AdminPermission, IsAdminOrReadOnly,
                          IsModeratorAutherAdminOrReadOnly, OwnPermission,
                          ReadOnly)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ProfileSerializer,
    ReviewSerializer, TitleCreateSerializer,
    TitleListSerializer, TokenObtainSerializer,
    UserCreateSerializer, UserSerializer
)
from .utils import send_confirmation_email


class EmailConfirmationViewSet(CreateViewSet):
    """Create user and send email with confirmation code if user exist
    only send email with confirmation code.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if user is None:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                user = serializer.instance
        refresh = RefreshToken.for_user(user)
        send_confirmation_email(str(refresh), user.email)
        return Response(
            {
                'username': request.data.get('username'),
                'email': request.data.get('email')
            },
            status=status.HTTP_200_OK
        )


class ObtainTokenView(TokenRefreshView):
    """Obtain token by username and confirmation code."""
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainSerializer


class UserViewSet(viewsets.ModelViewSet):
    """CRUD for user model."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    lookup_field = 'username'
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)


class ProfileViewSet(RetrievePatchViewSet):
    """Getting and patching your own profile."""
    serializer_class = ProfileSerializer
    permission_classes = (OwnPermission,)
    queryset = User.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            self.queryset,
            username=self.request.user.username
        )
        self.check_object_permissions(self.request, obj)
        return obj


class TitlesViewSet(ModelViewSet):
    """Viewset Title."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """Viewset Category."""
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)


class GenreViewSet(CreateListDestroyViewSet):
    """Viewset Genre."""
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)


class CommentViewSet(ModelViewSet):
    """ViewSet Comment"""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsModeratorAutherAdminOrReadOnly]

    def get_queryset(self):
        """Get Comment list with Review related"""
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title_id=title_id)
        return review.comments.all()

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(ModelViewSet):
    """ViewSet Review"""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsModeratorAutherAdminOrReadOnly]

    def get_queryset(self):
        """Get Review list with Title related"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)
