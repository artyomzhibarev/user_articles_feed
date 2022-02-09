from django.urls import path
from feed import views

urlpatterns = [
    path('api/v1/articles/', views.ArticleList.as_view()),
    path('api/v1/articles/<int:pk>/', views.ArticleDetail.as_view()),
]