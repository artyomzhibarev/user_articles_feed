from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import django.contrib.auth.password_validation as validators
from django.core import exceptions

from feed.models import Article, User


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Article
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=69, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=150, min_length=4),

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': _('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=69,
                                     min_length=settings.MIN_LENGTH_PASSWORD,
                                     write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')