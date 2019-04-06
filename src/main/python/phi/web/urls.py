from django.conf.urls import url

from . import views

urlpatterns = [
    url('index', views.index, name='index'),
    url('upload', views.upload, name='upload'),
    url('preview', views.preview, name='preview')
]
