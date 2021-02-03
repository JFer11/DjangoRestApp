from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_articles.models import CustomUser
from app_articles.serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout



def example(request):
    return HttpResponse("Hello")


class UserCreateOneOrGetAll(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request):
        users_list = CustomUser.objects.all()
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user(username):
    if CustomUser.objects.filter(username=username).exists():
        return CustomUser.objects.get(username=username)
    else:
        return None


class UserGetOnePutOneDeleteOne(APIView):
    """
    List one user, or edit a user.
    """

    def get(self, request, username):
        user = get_user(username)
        if user is None:
            return Response("The given user was not found!", status=status.HTTP_404_NOT_FOUND)
        user_serialized = UserSerializer(user)
        return Response(user_serialized.data)

    def put(self, request, username):
        user = get_user(username)
        if user is None:
            return Response("The given user was not found!", status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
Ignore above, in process...
class UserLogin(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Donde se guarda las sessions/cookies de login, es sessiondi?
                # Esta bien acceder a traves de request.COOKIES?
                login(request, user)
                return Response('ADENTRO')
            else:
                return Response('afuerraaa')
"""
