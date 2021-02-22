from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .exceptions import UserNotFound
from .models import CustomUser, Article, UserManager, ArticleComment


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


class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['id', 'message', 'created', 'updated', 'likes', 'dislikes', 'is_reply',
                  'article', 'author_comment', 'comment_reply']
        read_only_fields = ['author_comment', 'likes', 'dislikes']  # 'id', 'created' and 'updated', are already read_only.

    """Once the comment is POSTed, users may not be able to edit article's field."""
    def validate_article(self, value):
        if self.instance and self.instance.article != value:
            raise ValidationError("You may not edit the article. Try to remove the comment and create a new one for "
                                  "the new Article.")
        return value

    def validate_is_reply(self, value):
        if self.instance and value and self.instance.comment_reply is None:
            raise ValidationError("If is a comment reply, you have to explicit which article it replies.")
        return value

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
        validated_data['author_comment'] = CustomUser.objects.get(username=self.context['request'].user.username)
        return super().create(validated_data)
