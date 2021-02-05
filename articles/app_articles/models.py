# For Token Authentication
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# For Models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin

# RESPONDER LOS GITS COMMENTS


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('There must be a password')
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """
        DOUBT: WHAT HAPPENED WITH THE REST OF THE FIELDS THAT ARE IN REQUIRED_FIELDS BUT ARE NOT PASSED AS PARAMETERS.
        Solution: There are set as default.
        """
        """
        create_user must receive all parameters from required fields.
        Not only the REQUIRED_FIELDS, but also USERNAME_FIELD and password (Remember: are required by default)
        """

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Doubt: Fields are required, but not in serializer, so what happends here?
    # Doubt: if I send a field in a post request, and said field is not in attribute
    # 'fields' in serializer class, won t work.
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField('email address', max_length=255, unique=True)
    confirmed_email = models.BooleanField(default=False)
    # Para que demonios se usa el is_staff y is_active?
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # DOUBT: If I comment the line below, and I use the boolean field is_superuser from PermissionsMixin, it does
    # not appear in the AdminPage.
    is_superuser = models.BooleanField(default=False)  # It is commented because now it is provided by PermissionsMixin
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    updated = models.DateTimeField(auto_now=True)
    birth = models.DateTimeField()
    JUNIOR = 'JR'
    MID_LEVEL = 'MID'
    SENIOR = 'SR'
    LEVEL = (
        (JUNIOR, 'Junior'),
        (MID_LEVEL, 'Mid-level'),
        (SENIOR, 'Senior')
    )
    level = models.CharField(max_length=3, choices=LEVEL)
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['email', 'birth', 'level', 'gender']  # Will play in python manage.py cratesuperuser

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    """
    This would be necessary if PermissionsMixin was not inherited
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    """

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    What is this? Well, every time we call the save() method from a Model, two signals are sent. One at the beginning
    of the method, an another at the end.
    post_save is the name of the signal that runs at the end of the method save().
    What are we doing here? @receiver allows us to execute a function after the selected signal (post_save in our case)
    has been sent. Moreover, the function will be executed if the signal is send with sender argument
    as settings.AUTH_USER_MODEL.
    So, summarising, every time a CustomUser is created, this function will be executed and a token for the recently
    created User is created.
    """
    if created:
        """Remember that we can call save() method when we want to update a model, here we verify we are creating 
        said model, and not updating it."""
        Token.objects.create(user=instance)


class Article(models.Model):
    title = models.CharField(max_length=30, unique=True, null=False)
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    """DOUBT: I thought that models.ForeignKey saves integers ids. However, in serializers.py I created the field
    as a CharField and a username was shown. I have an idea about what is probably happening here. When I create an 
    'Article' I have to give a CustumUser model, not the id (we can do Article.author.first_name). So, when I 
    serialize 'Articles', the author field, instead of represent the CustomUser.id, represents the whole object.
    And the whole object is represented through __str__ method, which is defined to return the username.   
    """
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
