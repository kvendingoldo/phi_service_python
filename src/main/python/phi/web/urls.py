from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    re_path(r'documents', views.DocumentsView.as_view(), name='list'),
    re_path(r'^document/(?P<pk>.+)$', views.DocumentView.as_view(), name='document-detail'),



    url('index', views.index, name='index'),
    url('upload', views.upload, name='upload'),
    url('preview', views.preview, name='preview'),
    path('admin/', admin.site.urls),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout')
]