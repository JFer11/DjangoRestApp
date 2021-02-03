from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_articles.models import Article
from app_articles.serializers import ArticleSerializer


class ArticleCreateOneOrGetAll(APIView):
    """
    List all article, or create a new user.
    """

    def get(self, request):
        articles_list = Article.objects.all()
        serializer = ArticleSerializer(articles_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_article(pk):
    try:
        return Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return None


class ArticleGetOnePutOneDeleteOne(APIView):
    """
    List one articles, or edit an 'Article'.
    """

    def get(self, request, pk):
        article = get_article(pk)
        if article is None:
            return Response(f"The article with id={pk} does not exist.", status=status.HTTP_404_NOT_FOUND)

        article_serialized = ArticleSerializer(article)
        return Response(article_serialized.data)

    def put(self, request, pk):
        article = get_article(pk)
        if article is None:
            return Response(f"The article with id={pk} does not exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
