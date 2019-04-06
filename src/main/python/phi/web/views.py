from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def upload(request):
    return HttpResponse("Upload page")


def preview(request):
    return HttpResponse("Preview page")
