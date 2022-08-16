from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from api.functions import get_today


# System Models
class SystemUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, commit=True):

        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):

        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = models.CharField(verbose_name='Username', max_length=150, unique=True)

    # Profile data - TODO images?
    prof_image = models.ImageField(verbose_name='Profile Image', upload_to='profs', max_length=None, blank=True)
    prof_desc = models.TextField(verbose_name='Profile Desc', blank=True)
    followers = models.IntegerField(verbose_name='Followers', blank=True, default=0)
    following = models.IntegerField(verbose_name='Following', blank=True, default=0)

    # Admin data
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_staff = models.BooleanField('Admin Status', default=False)
    date_joined = models.DateTimeField(verbose_name='Date Joined', default=get_today)
    last_login = models.DateTimeField(verbose_name='Last Login', default=get_today)

    # Spare Fields
    field1 = models.CharField(max_length=255, default="", blank=True)
    field2 = models.CharField(max_length=255, default="", blank=True)
    field3 = models.CharField(max_length=255, default="", blank=True)
    field4 = models.CharField(max_length=255, default="", blank=True)
    field5 = models.CharField(max_length=255, default="", blank=True)

    objects = SystemUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_title(self):
        return '{} <{}>'.format(self.username, self.email)

    def __str__(self):
        return self.get_title()


# Models
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=get_today)
    last_edit = models.DateTimeField(default=get_today)
    last_update = models.DateTimeField(default=get_today)

    content = models.TextField(default="")
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    image_post = models.BooleanField(default=False)
    image_contents = models.ImageField(upload_to='posts', max_length=None, blank=True)

    # Spare Fields
    field1 = models.CharField(max_length=255, default="", blank=True)
    field2 = models.CharField(max_length=255, default="", blank=True)
    field3 = models.CharField(max_length=255, default="", blank=True)
    field4 = models.CharField(max_length=255, default="", blank=True)
    field5 = models.CharField(max_length=255, default="", blank=True)

    def get_all_objects(self):
        queryset = self._meta.model.objects.all()
        return queryset

    def __str__(self):
        return "Post {} by {}".format(self.id, self.created_by.username)


class Follow(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_user")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    created_date = models.DateTimeField(default=get_today)

    # Spare Fields
    field1 = models.CharField(max_length=255, default="", blank=True)
    field2 = models.CharField(max_length=255, default="", blank=True)
    field3 = models.CharField(max_length=255, default="", blank=True)
    field4 = models.CharField(max_length=255, default="", blank=True)
    field5 = models.CharField(max_length=255, default="", blank=True)

    def get_all_objects(self):
        queryset = self._meta.model.objects.all()
        return queryset

    def __str__(self):
        return "({}) {} followed by {}".format(self.id, self.following.username, self.created_by.username)


class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    created_date = models.DateTimeField(default=get_today)

    # Spare Fields
    field1 = models.CharField(max_length=255, default="", blank=True)
    field2 = models.CharField(max_length=255, default="", blank=True)
    field3 = models.CharField(max_length=255, default="", blank=True)
    field4 = models.CharField(max_length=255, default="", blank=True)
    field5 = models.CharField(max_length=255, default="", blank=True)

    def get_all_objects(self):
        queryset = self._meta.model.objects.all()
        return queryset

    def __str__(self):
        return "({}) Post {} liked by {}".format(self.id, self.post.id, self.created_by.username)