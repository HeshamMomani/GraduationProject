from django.contrib.auth.models import AbstractUser, BaseManager
from django.db import models


class CustomUserManager(BaseManager):
    def create_user(self, email, first_name, last_name, username, usertype, password=None):
        # Create and save a regular user with the given email and password
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, usertype=usertype,
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        if self.model.objects.filter(email=email).exists():
            raise ValueError('This email already exists')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, usertype='admin')
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    USERTYPE_CHOICES = (
        ('provider', 'Service Provider'),
        ('recipient', 'Service Recipient'),
        ('admin', 'Administrator'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    usertype = models.CharField(max_length=22, choices=USERTYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
