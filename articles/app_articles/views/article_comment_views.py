from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app_articles.paginations import ArticleCommentsPagination
from app_articles.serializers import ArticleCommentSerializer, ReplyCommentSerializer
from app_articles.models import ArticleComment


class ArticleCommentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Article Comments.
    """
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ArticleCommentsPagination


class ReplyCommentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Article reply comments.
    """
    queryset = ArticleComment.objects.filter(is_reply=True)
    serializer_class = ReplyCommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ArticleCommentsPagination
