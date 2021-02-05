from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from app_articles.models import CustomUser
from app_articles.serializers import UserSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing CustomUsers.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # retrieve() was override because we want to return a User depending on the username, not the id
    def retrieve(self, request, *args, **kwargs):
        # DOUBT: How to save the pk as username directly
        username = kwargs['pk'] if len(kwargs) == 1 else None
        users_list = CustomUser.objects.all()
        user = get_object_or_404(users_list, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    # update() was override because we want to return a User depending on the username, not the id
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        username = kwargs['pk'] if len(kwargs) == 1 else None
        users_list = CustomUser.objects.all()
        instance = get_object_or_404(users_list, username=username)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


"""
EXAMPLE OF SIMPLE VIEWS:

class UserCreateOneOrGetAll(APIView):
    ""
    # List all users, or create a new user.
    ""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        users_list = CustomUser.objects.all()
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
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
    ""
    List one user, or edit a user.
    ""

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
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
