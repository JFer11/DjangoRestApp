from rest_framework.permissions import BasePermission
from app_articles.models import Article


class PublicArticleOrLoggedUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        pk_article = request.parser_context['kwargs']['pk']
        article = Article.objects.get(pk=pk_article)

        if article.is_public:
            return True
        else:
            return bool(request.user and request.user.is_authenticated)
