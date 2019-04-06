from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url


urlpatterns = [
    url(r'^web/', include('web.urls')),
    path('admin/', admin.site.urls),
]
