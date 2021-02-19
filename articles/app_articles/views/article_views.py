from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app_articles.paginations import MyPaginationArticles
from app_articles.serializers import ArticleSerializer
from app_articles.models import Article


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Articles.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPaginationArticles

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
