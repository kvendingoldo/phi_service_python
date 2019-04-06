# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

from .forms import UploadFileForm
from .models import Document

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def preview(request):
    return HttpResponse("Preview page")


@login_required(login_url='/accounts/login/')
def index_files(request):
    files = Document.objects.all()
    return render(request, 'index_files.html', {'files': files})


@login_required(login_url='/accounts/login/')
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('/Users/asharov/dj.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)