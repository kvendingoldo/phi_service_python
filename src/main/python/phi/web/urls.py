from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('index', views.index, name='index'),
    url('upload', views.upload, name='upload'),
    url('preview', views.preview, name='preview'),
    path('admin/', admin.site.urls),
    url(r'^register/$', views.register, name='register'),
    #url('^', include('django.contrib.auth.urls'))
    url('^accounts/', include('django.contrib.auth.urls'))
]
