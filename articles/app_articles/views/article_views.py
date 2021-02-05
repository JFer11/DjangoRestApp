from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app_articles.serializers import ArticleSerializer
from app_articles.models import Article


class ArticleCreateOneOrGetAll(APIView):
    """
    List all article, or create a new user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        articles_list = Article.objects.all()
        serializer = ArticleSerializer(articles_list, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'Error': 'Given title already exists'}, status=status.HTTP_400_BAD_REQUEST)
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

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        article = get_article(pk)
        if article is None:
            return Response(f"The article with id={pk} does not exist.", status=status.HTTP_404_NOT_FOUND)

        article_serialized = ArticleSerializer(article, context={'request': request})
        return Response(article_serialized.data)

    def put(self, request, pk):
        article = get_article(pk)
        if article is None:
            return Response(f"The article with id={pk} does not exist.", status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'Error': 'Given title already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
