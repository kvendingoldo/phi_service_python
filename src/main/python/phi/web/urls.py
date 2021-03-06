from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url

from . import views

urlpatterns = [
    re_path(r'^document/(?P<pk>.+)$', views.document_view, name='document-detail'),
    url('index', views.DocumentsView.as_view(), name='index'),
    url('upload', views.upload, name='upload'),
    path('admin/', admin.site.urls),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
