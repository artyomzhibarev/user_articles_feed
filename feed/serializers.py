from rest_framework import serializers

from feed.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Article
        fields = '__all__'
        # exclude = ['is_public', 'id']
