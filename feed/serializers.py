from django.contrib.auth import authenticate
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
        fields = ['id', 'author', 'content', 'title', 'created_at', 'updated_at', 'is_public']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=69, min_length=settings.MIN_LENGTH_PASSWORD, write_only=True)
    email = serializers.EmailField(max_length=150, min_length=4)

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


# class LoginSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         max_length=69, min_length=settings.MIN_LENGTH_PASSWORD, write_only=True)
#     email = serializers.EmailField(max_length=150, min_length=4)
#
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def validate(self, attrs):
#         username = attrs.get('email')
#         password = attrs.get('password')
#         # {"email": "user2@user2.com", "password": "1q2w3e4r5"}
#
#         if username and password:
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)
#             if not user:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = _('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')
#
#         attrs['user'] = user
#         return attrs
