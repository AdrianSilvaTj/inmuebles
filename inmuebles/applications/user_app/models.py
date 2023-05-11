# from django.db.models.signals import post_save
# from django.conf import settings
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

# """ Crea el token automaticamente al crearse un usuario. """
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email.')
        if not username:
            raise ValueError('El usuario debe tener un username.')
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number = phone_number,
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, phone_number, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            password=password,
            username=username,
            phone_number = phone_number,
            email=self.normalize_email(email),
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number']
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True