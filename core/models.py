from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class Product(models.Model):
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    quantity = models.IntegerField()
    def __str__(self):
        return self.description
class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Usuários precisam ter um endereço de email")
        if not username:
            raise ValueError("Usuários precisam ter um nome de usuário (username)")

        user = self.model(
                email=self.normalize_email(email), #converte todos os caracteres do email pra minusculo
                username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
                email=self.normalize_email(email), #converte todos os caracteres do email pra minusculo
                username = username,
                password = password,
        )
        user.is_admin =  True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email",max_length=60,unique=True)
    username        = models.CharField(max_length=30,unique=True)
    date_joined     = models.DateTimeField(verbose_name="Data de adesão",auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="Ultimo login",auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    first_name      = models.CharField(verbose_name="Nome", max_length=30)
    last_name       = models.CharField(verbose_name="Sobrenome",max_length=30)
    cpf             = models.CharField(verbose_name="CPF", max_length=11)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __Str__(self):
        return self.username + ", " + self.email
    def has_perm(self,perm,obj = None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
