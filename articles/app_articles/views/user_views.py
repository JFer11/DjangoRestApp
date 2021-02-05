from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from app_articles.models import CustomUser
from app_articles.serializers import UserSerializer


def example(request):
    return HttpResponse("Hello")


class UserCreateOneOrGetAll(APIView):
    """
    List all users, or create a new user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        users_list = CustomUser.objects.all()
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
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

    permission_classes = [IsAuthenticated]

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


class LoginCustomAuthToken(ObtainAuthToken):
    """
    Login view. We had to override POST method.

    Remember that the serializer in ObtainAuthToken has 'validate' method overwritten, and inside
    validate(), authenticate method is used.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # is_valid checks if username and password are correct.
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # DOUBT:  I do not get why serializer.data is an empty dict, if serializer fields are username, password and
        # token. Username and password are write_only=True, perfect, however, token is read_only and it does not appear.
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })
