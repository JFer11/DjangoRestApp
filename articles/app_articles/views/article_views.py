from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app_articles.exceptions import NullRequest
from app_articles.paginations import ArticlesPagination
from app_articles.permissions import PublicArticleOrLoggedUser
from app_articles.serializers import ArticleSerializer
from app_articles.models import Article


def is_logged(request):
    return bool(request.user and request.user.is_authenticated)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Articles.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlesPagination

    def get_asc_or_desc(self, request, queryset):
        if request is None:
            raise NullRequest

        order = request.headers.get('Sort', None)
        if order == 'DESC':
            queryset = queryset.order_by('-created')
        elif order == 'ASC':
            queryset = queryset.order_by('created')
        elif order is None:
            # No order requested
            # Default:
            queryset = queryset.order_by('-created')
        return queryset

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        # what I added:
        queryset = self.get_asc_or_desc(self.request, self.queryset)

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['retrieve']:
            permission_classes = [PublicArticleOrLoggedUser]
        elif self.action in ['list']:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        # what I added:
        if not is_logged(request):
            queryset = queryset.filter(is_public=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

