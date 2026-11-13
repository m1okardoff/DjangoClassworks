from django.contrib.auth.hashers import make_password
from django.db import models


# Create your models here.

class Card(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='cards/')
    created_at = models.DateTimeField()


class User(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="Ім'я користувача")
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватарка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.username
