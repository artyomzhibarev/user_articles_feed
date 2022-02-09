from django.contrib import admin
from .models import User, Article


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined')
    list_filter = ('date_joined',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created_at', 'updated_at', 'is_public', )
    list_filter = ('created_at', 'is_public', )
    list_editable = ('is_public', 'title')
