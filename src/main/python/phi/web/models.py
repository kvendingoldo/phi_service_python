from djongo import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class User(models.Model):
    name = models.TextField()
    meta = models.TextField()
    hash = models.TextField()


class Document(models.Model):
    _id = models.ObjectIdField()
    owner = models.CharField(max_length=20)
    title = models.TextField()
    meta = models.TextField()
    body = models.TextField()

    def get_absolute_url(self):
        return "/document/%s" % self._id


class DocumentDecryptedMeta:
    def __init__(self, title, date, comments):
        self.title = title
        self.date = date
        self.comments = comments


class View(models.Model):
    owner = models.CharField(max_length=20)
    meta = models.TextField()
    structure = models.TextField()
