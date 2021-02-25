from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app_articles.paginations import ArticleCommentsPagination
from app_articles.serializers import ArticleCommentSerializer
from app_articles.models import ArticleComment


class ArticleCommentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Article Comments.
    """
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ArticleCommentsPagination

    """def get_serializer_class(self):
        # if self.action == 'list':
        #     return serializers.ListaGruppi

        return ArticleCommentSerializer
    """