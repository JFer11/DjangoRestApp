from django.contrib import admin
from django.urls import path
from app_articles.views.user_views import UserViewSet
from app_articles.views.article_views import ArticleViewSet
from app_articles.views.article_comment_views import ArticleCommentViewSet
from rest_framework.routers import DefaultRouter
from app_articles.views import user_views

"""
urlpatterns = [
    path('api/article/', article_views.ArticleCreateOneOrGetAll.as_view(), name='user_no_id'),
    path('api/article/<int:pk>', article_views.ArticleGetOnePutOneDeleteOne.as_view(), name='user_id'),
]
"""


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'articles-comments', ArticleCommentViewSet, basename='article_comment')
urlpatterns = router.urls
urlpatterns.append(path('admin/', admin.site.urls))
urlpatterns.append(path('api/login/', user_views.LoginCustomAuthToken.as_view(), name='user_login'))
