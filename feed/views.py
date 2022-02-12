from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import logout

from feed.permissions import IsOwnerOrReadOnly, IsSubscriberOrReadOnly
from feed.serializers import ArticleSerializer, Article, UserSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsSubscriberOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        print(f'Groups: {self.request.user.groups.all()}')
        print(f'User: {request.user}')
        if self.request.user.groups.filter(name='subscribers').exists():  # указать это в permissions.py
            return super().list(request)  # if the user is in a subscribers group
        queryset = self.get_queryset()
        queryset = queryset.filter(is_public=True)
        serializer = ArticleSerializer(queryset, many=True)  # if not, then show only public articles
        return Response(data=serializer.data)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        print(f'Groups: {self.request.user.groups.all()}')
        print(f'User: {request.user}')
        return self.retrieve(request, *args, **kwargs)


class RegisterUser(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasicAuthUser(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
            'message': f'User {request.user} has been successfully authorized'
        }
        return Response(data=content)


class BasicLogOut(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]

    def get(self, request):
        user = request.user
        print(f'User {user} successfully logged out')
        logout(request)
        print(request.user)
        return Response(data={'message': f'User {user} successfully logged out'},
                        status=status.HTTP_200_OK)
