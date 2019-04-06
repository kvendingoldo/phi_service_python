from django.db import models

# Create your models here.


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    meta = models.TextField()

    def publish(self):
        self.save()


class Document(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    owner = models.CharField(max_length=20)
    meta = models.TextField()
    body = models.TextField()

    def publish(self):
        self.save()


class View(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    owner = models.CharField(max_length=20)
    meta = models.TextField()
    structure = models.TextField()

    def publish(self):
        self.save()
