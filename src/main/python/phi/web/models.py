from djongo import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class User(models.Model):
    meta = models.TextField()


class Document(models.Model):
    owner = models.CharField(max_length=20)
    meta = models.TextField()
    body = models.TextField()

    def get_absolute_url(self):
        return "/document/%i" % self.id


class View(models.Model):
    owner = models.CharField(max_length=20)
    meta = models.TextField()
    structure = models.TextField()
