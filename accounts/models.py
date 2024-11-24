from django.db import models
from django.contrib.auth.models import AbstractUser


# 커스텀 유저모델
class User(AbstractUser):
    GENDER_CHOICES = [
        ("M", "남성"),
        ("F", "여성"),
        ("O", "기타"),
    ]

    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    email = models.EmailField(max_length=30, unique=True)
    nickname = models.CharField(max_length=30)
    birthday = models.DateField()
    introduction = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.username

    def soft_delete(self):
        self.is_active = False
        self.save()
