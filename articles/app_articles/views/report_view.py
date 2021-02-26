from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from app_articles.models import Article
from app_articles.serializers import UserSerializer


class ReportViewOneArticle(APIView):

    def post(self, request, article_id):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return Response({"Error": f"Article with ID: {article_id} does not exist."}, status=HTTP_404_NOT_FOUND)

        if self.request.user in article.users_reports.all():
            return Response({"Error": f"Article with ID: {article_id} was already reported by"
                                      f"you, {self.request.user}."}, status=HTTP_400_BAD_REQUEST)
        else:
            article.users_reports.add(self.request.user)
            return Response({"Success": f"You, the user {self.request.user} has successfully reported the article"
                                        f" with ID: {article_id}. Thanks!"})

    def get(self, request, article_id):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return Response({"Error": f"Article with ID: {article_id} does not exist."}, status=HTTP_404_NOT_FOUND)

        users = article.users_reports.all()
        users = UserSerializer(users, many=True)

        return Response(
            {
                f"Reports for Article {article_id}": len(users.data),
                f"Users": users.data
            }
        )


class ReportViewAll(APIView):

    def get(self, request):
        response = {}

        articles = Article.objects.all()

        for article in articles:
            users = article.users_reports.all()
            users = UserSerializer(users, many=True)
            response[article.pk] = {
                f"Reports for Article {article.pk}": len(users.data),
                f"Users": users.data
            }
        return Response(response)
