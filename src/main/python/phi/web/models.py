from django.db import models

# Create your models here.


class User(models.Model):
    meta = models.TextField()


class Document(models.Model):
    owner = models.CharField(max_length=20)
    meta = models.TextField()
    body = models.TextField()


class View(models.Model):
    owner = models.CharField(max_length=20)
    meta = models.TextField()
    structure = models.TextField()
