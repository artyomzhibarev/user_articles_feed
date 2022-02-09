from rest_framework import generics
from rest_framework.response import Response
from feed.permissions import IsOwnerOrReadOnly, IsSubscriberOrReadOnly
from feed.serializers import ArticleSerializer, Article
# user2@user2.com 1q2w3e4r5
# admin@admin.com 1


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsSubscriberOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='subscribers').exists():
            return super().list(request)  # if the user is in a subscribers group
        queryset = self.get_queryset()
        queryset = queryset.filter(is_public=True)
        serializer = ArticleSerializer(queryset, many=True)  # if not, then show only public articles
        return Response(serializer.data)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
