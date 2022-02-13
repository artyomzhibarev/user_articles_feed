from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView

from feed.permissions import IsOwnerOrReadOnly, IsSubscriberOrReadOnly
from feed.serializers import ArticleSerializer, Article, UserSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsSubscriberOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='subscribers').exists():
            queryset = self.get_queryset()
        else:
            queryset = self.get_queryset().filter(is_public=True)
        serializer = ArticleSerializer(queryset, many=True)

        return Response(data=serializer.data)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]


class RegisterUser(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasicAuthUser(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        msg = {'message': f'{request.user.email} successfully authenticated!'}
        return Response(msg, status=status.HTTP_200_OK)


class BasicLogOut(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        logout(request)
        return Response(data={'message': f'User {user} successfully logged out'},
                        status=status.HTTP_200_OK)
