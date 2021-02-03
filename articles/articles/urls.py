"""articles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_articles.views import user_views, article_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.example, name='example'),
    path('api/user/', user_views.UserCreateOneOrGetAll.as_view(), name='user_no_username'),
    path('api/user/<str:username>', user_views.UserGetOnePutOneDeleteOne.as_view(), name='user_username'),
    path('api/article/', article_views.ArticleCreateOneOrGetAll.as_view(), name='user_no_id'),
    path('api/article/<int:pk>', article_views.ArticleGetOnePutOneDeleteOne.as_view(), name='user_id'),
    path('api/user/login', user_views.UserLogin.as_view(), name='user_login'),
]
