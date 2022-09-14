from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Username already exist')
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Email already exist')
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                {'username': ['Invalid username: me']})
        return data


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
    token = serializers.ReadOnlyField()

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        try:
            refresh = RefreshToken(data.get('confirmation_code'))
        except TokenError as error:
            raise serializers.ValidationError(
                {'confirmation_code': error})
        if user.id != refresh.payload.get('user_id'):
            raise serializers.ValidationError(
                {'error': ['Wrong username or code']})
        return {'token': str(refresh.access_token)}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role',)
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.ChoiceField(choices=settings.REVIEW_SCORE)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            reviews = self.context.get('request').user.reviews.all()
            if reviews.filter(title_id=title_id):
                raise serializers.ValidationError("several review not allow")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title
