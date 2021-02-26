from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

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
        fields = ['id', 'title', 'text', 'created', 'updated', 'author', 'is_public']
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
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


# TODO TENGO QUE SEPARAR EN RESPONDER ARTICULOS Y RESPONDER COMENTARIOS
class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['id', 'message', 'created', 'updated', 'likes', 'dislikes',
                  'article', 'author_comment', 'is_reply', 'comment_reply']
        # 'id', 'created', 'updated' and are already read_only.
        read_only_fields = ['author_comment', 'likes', 'dislikes', 'is_reply', 'comment_reply']

    def validate_article(self, value):
        """Once the comment is POSTed, users may not be able to edit article's field."""
        if self.instance and self.instance.article != value:
            raise ValidationError("You may not edit the article. Try to remove the comment and create a new one for "
                                  "the new Article.")
        return value

    def validate(self, attrs):
        # ""Use this method to validate across multiple fields""
        return super().validate(attrs)

    """
    Representation:
    -----------------------------------------------------------
    ArticleCommentSerializer():
        id = IntegerField(label='ID', read_only=True)
        message = CharField(style={'base_template': 'textarea.html'})
        created = DateTimeField(read_only=True)
        updated = DateTimeField(read_only=True)
        likes = IntegerField(read_only=True)
        dislikes = IntegerField(read_only=True)
        article = PrimaryKeyRelatedField(queryset=Article.objects.all())
        author_comment = PrimaryKeyRelatedField(read_only=True)
    -----------------------------------------------------------
    print(repr(ArticleCommentSerializer()))
    """

    def create(self, validated_data):
        # Author_comment is a read_only field, here we set the author depending on the user who is making the request.
        validated_data['author_comment'] = CustomUser.objects.get(username=self.context['request'].user.username)
        return super().create(validated_data)


class ReplyCommentSerializer(serializers.ModelSerializer):

    comment_reply = PrimaryKeyRelatedField(allow_null=False, queryset=ArticleComment.objects.all(), required=True)

    class Meta:
        model = ArticleComment
        fields = ['id', 'message', 'comment_reply',
                  'created', 'updated', 'likes', 'dislikes', 'article', 'author_comment', 'is_reply']
        # 'id', 'created', 'updated' and are already read_only.
        read_only_fields = ['likes', 'dislikes', 'article', 'author_comment', 'is_reply']

    def validate_comment_reply(self, value):
        """Once the comment is POSTed, users may not be able to edit comment_reply's field."""
        if self.instance and self.instance.comment_reply != value:
            raise ValidationError("You may not edit the article. Try to remove the comment and create a new one for "
                                  "the new Article.")
        return value
    """
    # TODO: Porque pasa esto?
    def validate_comment_reply(self, value):
        # ""Note, value here is: <ArticleComment: <id>>. Is already validated.""
        # TODO: Donde se evalua que el objeto exista.
        return value
    """
    """
    Representation:
    -----------------------------------------------------------
    ReplyCommentSerializer():
        id = IntegerField(label='ID', read_only=True)
        message = CharField(style={'base_template': 'textarea.html'})
        comment_reply = PrimaryKeyRelatedField(allow_null=False, queryset=ArticleComment.objects.all(), required=True)
        created = DateTimeField(read_only=True)
        updated = DateTimeField(read_only=True)
        likes = IntegerField(read_only=True)
        dislikes = IntegerField(read_only=True)
        article = PrimaryKeyRelatedField(read_only=True)
        author_comment = PrimaryKeyRelatedField(read_only=True)
        is_reply = BooleanField(read_only=True)

    -----------------------------------------------------------
    print(repr(ReplyCommentSerializer()))
    """

    def create(self, validated_data):
        # Author_comment is a read_only field, here we set the author depending on the user who is making the request.
        validated_data['author_comment'] = CustomUser.objects.get(username=self.context['request'].user.username)
        validated_data['is_reply'] = True
        validated_data['article'] = validated_data['comment_reply'].article
        return super().create(validated_data)

