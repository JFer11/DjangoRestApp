from rest_framework import serializers

from .exceptions import UserNotFound
from .models import CustomUser, Article, UserManager


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
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        del validated_data['username']
        del validated_data['email']
        del validated_data['password']
        return CustomUser.objects.create_user(username, email, password, **validated_data)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'created', 'updated', 'author']
        read_only_fields = ['author']  # 'id', 'created' and 'updated', are already read_only.

    """
    Representation:
    -----------------------------------------------------------
    ArticleSerializer():
        id = IntegerField(label='ID', read_only=True)
        title = CharField(max_length=30, validators=[<UniqueValidator(queryset=Article.objects.all())>])
        text = CharField(style={'base_template': 'textarea.html'})
        created = DateTimeField(read_only=True)
        updated = DateTimeField(read_only=True)
        author = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    -----------------------------------------------------------
    """

    def create(self, validated_data):
        validated_data['author'] = CustomUser.objects.get(username=self.context['request'].user.username)
        return super().create(validated_data)
