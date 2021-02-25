from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework.validators import UniqueTogetherValidator

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

"""
class ArticleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleComment
        fields = ['id', 'message', 'created', 'updated', 'likes', 'dislikes', 'is_reply',
                  'article', 'author_comment', 'comment_reply']
        # 'id', 'created', 'updated' and 'is_reply', are already read_only.
        read_only_fields = ['author_comment', 'likes', 'dislikes']

    def is_a_comment_reply(self, obj):
        return 'comment_reply' in self.context['request'].data

    is_reply = serializers.SerializerMethodField(method_name='is_a_comment_reply')

    def validate_article(self, value):
        # ""Once the comment is POSTed, users may not be able to edit article's field.""

        if self.instance and self.instance.article != value:
            raise ValidationError("You may not edit the article. Try to remove the comment and create a new one for "
                                  "the new Article.")
        return value

    def validate_comment_reply(self, value):
        # ""Once the comment is POSTed, users may not be able to edit comment_reply field.""

        if self.instance and self.instance.article != value:
            raise ValidationError("You may not edit the comment that you are replying. "
                                  "Try to remove the comment and create a new one reply to the comment the new"
                                  " comment.")
        return value

    def validate(self, attrs):
        # ""Use this method to validate across multiple fields""
        return super().validate(attrs)


    #""
    #Representation:
    #-----------------------------------------------------------
    
    #-----------------------------------------------------------
    #""
    def create(self, validated_data):
        # Author_comment is a read_only field, here we set the author depending on the user who is making the request.
        validated_data['author_comment'] = CustomUser.objects.get(username=self.context['request'].user.username)
        return super().create(validated_data)
"""

# TODO TENGO QUE SEPARAR EN RESPONDER ARTICULOS Y RESPONDER COMENTARIOS


class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['id', 'message', 'created', 'updated', 'likes', 'dislikes',
                  'article', 'author_comment']
        # 'id', 'created', 'updated' and are already read_only.
        read_only_fields = ['author_comment', 'likes', 'dislikes']

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

    -----------------------------------------------------------
    """
    def create(self, validated_data):
        # Author_comment is a read_only field, here we set the author depending on the user who is making the request.
        validated_data['author_comment'] = CustomUser.objects.get(username=self.context['request'].user.username)
        return super().create(validated_data)


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment


    def validate_comment_reply(self, value):
        # ""Once the comment is POSTed, users may not be able to edit comment_reply field.""

        if self.instance and self.instance.article != value:
            raise ValidationError("You may not edit the comment that you are replying. "
                                  "Try to remove the comment and create a new one reply to the comment the new"
                                  " comment.")
        return value