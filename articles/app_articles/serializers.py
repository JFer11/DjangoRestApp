from rest_framework import serializers

from .exceptions import UserNotFound
from .models import CustomUser, Article


class UserSerializer(serializers.ModelSerializer):
    """
    FACT:
    Every not specified field in corresponding serializers, will not be taken into account, even if they are sent in the
    request body. If we do not want to show fields but be able to accepts them in a request, we need the write_only flag.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'gender', 'birth', 'level', 'is_staff',
                  'confirmed_email', 'is_active', 'is_superuser', 'password']
        extra_kwargs = {
            'is_staff': {'write_only': True},
            'confirmed_email': {'write_only': True},
            'is_active': {'write_only': True},
            'is_superuser': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ArticleSerializer(serializers.Serializer):
    """
    Model serializer provides create() and update() methods. We do not use model Serializer because 'author' field
    requires an object, and we want to send not an object (CustomUser), but the username.
    """

    def get_author(self, obj):
        return self.context['request'].user.username

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    text = serializers.CharField(style={'base_template': 'textarea.html'})
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    # SerializerMethodField is a read_only field, so we cannot access to it in create method. Instead, if
    author = serializers.SerializerMethodField(method_name='get_author')

    def create(self, validated_data):
        """
        Create and return a new `Article` instance, given the validated data.
        """

        """
        At first, everybody could create articles in name of anyone. A Username was provided through the request, and
        then, author filed was filled by querying the database with the given username.
        It was required to check if a user with given username exists, so said implementation wis below:
            These were the old fields:
            # author = serializers.CharField(max_length=30, read_only=True)
            # username = serializers.CharField(max_length=30, write_only=True)
        
        data = validated_data
        if CustomUser.objects.filter(username=validated_data.get('username')).exists():
            data['author'] = CustomUser.objects.get(username=validated_data.get('username'))
            del data['username']
        else:
            raise UserNotFound("Given user does not exist!")
        return Article.objects.create(**data)
        """
        # SerializerMethodField is a read_only field, so we cannot access to it directly. Instead, we have
        # get its content calling its function.
        validated_data['author'] = CustomUser.objects.get(username=self.get_author(None))
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Article` instance, given the validated data.
        """

        """
        At first, everybody could create articles in name of anyone. A Username was provided through the request, and
        then, author filed was filled by querying the database with the given username.
        It was required to check if a user with given username exists, so said implementation wis below:
            These were the old fields:
            # author = serializers.CharField(max_length=30, read_only=True)
            # username = serializers.CharField(max_length=30, write_only=True)
                
        if CustomUser.objects.filter(username=validated_data.get('username')).exists():
            instance.author = CustomUser.objects.get(username=validated_data.get('username'))
        else:
            instance.author = None

        """
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        # Author should not be edited when updating.
        instance.save()
        return instance
