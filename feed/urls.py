from django.urls import path
from feed import views

urlpatterns = [
    path('api/v1/articles/', views.ArticleList.as_view()),
    path('api/v1/articles/<int:pk>/', views.ArticleDetail.as_view()),
    path('api-auth/registration/', views.RegisterUser.as_view(), name='register'),
    # path('api/v1/auth/login/', views.BasicAuthUser.as_view(), name='login'),
    # path('api/v1/auth/logout/', views.BasicLogOut.as_view(), name='logout')
]
