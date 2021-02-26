from django.contrib import admin
from django.urls import path
from app_articles.views.user_views import UserViewSet, LoginCustomAuthToken
from app_articles.views.article_views import ArticleViewSet
from app_articles.views.report_view import ReportViewOneArticle, ReportViewAll
from app_articles.views.article_comment_views import ArticleCommentViewSet, ReplyCommentViewSet
from rest_framework.routers import DefaultRouter


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
router.register(r'reply/articles-comments', ReplyCommentViewSet, basename='reply_article_comment')
urlpatterns = router.urls
urlpatterns.append(path('admin/', admin.site.urls))
urlpatterns.append(path('api/login/', LoginCustomAuthToken.as_view(), name='user_login'))
urlpatterns.append(path('report/<int:article_id>', ReportViewOneArticle.as_view(), name='report_article_id'))
urlpatterns.append(path('report/', ReportViewAll.as_view(), name='report_article_all'))
