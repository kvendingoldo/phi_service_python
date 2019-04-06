from django.db import models

# Create your models here.


class User(object):
    def __init__(self):
        self.id = None
        self.meta = None


class Document(object):

    def __init__(self):
        self.id = None
        self.owner = None
        self.meta = None
        self.body = None


class View(object):

    def __init__(self):
        self.id = None
        self.owner = None
        self.meta = None
        self.structure = None
