# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import UploadFileForm, UserForm
from .models import Document, DocumentDecryptedMeta

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utils.cipher import AESCipher

import pickle
import codecs
import string
import random


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    aes_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'registration/registration.html',
                  {'user_form': user_form,
                   'registered': registered,
                   'aes_password': aes_password
                   })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'registration/login.html', {})


@login_required(login_url='/accounts/login/')
def preview(request):
    return HttpResponse("Preview page")


@login_required(login_url='/accounts/login/')
def index(request):
    files = Document.objects.all()
    return render(request, 'index.html', {'files': files})


@login_required(login_url='/accounts/login/')
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            key = form.files['key']
            if not check_key(key, request):
                return HttpResponseRedirect('failure/url')
            file = form.files['file']
            meta = DocumentDecryptedMeta(form.fields['title'], None, form.fields['comments'])
            handle_uploaded_file(file, meta, key, request)
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def check_key(key, request):
    return True


def handle_uploaded_file(file, meta, key, request):
    cipher = AESCipher(key.file.read().decode("utf-8"))

    pickled_file = codecs.encode(pickle.dumps(file), "base64").decode()
    file_enc = cipher.encrypt(pickled_file)

    pickled_meta = codecs.encode(pickle.dumps(meta), "base64").decode()
    meta_enc = cipher.encrypt(pickled_meta)

    document = Document(meta=meta_enc, body=file_enc, owner=request.user.id)
    document.save()


# @login_required(login_url='/accounts/login/')
class DocumentsView(ListView):
    model = Document

    template_name = 'index.html'

    queryset = Document.objects.all()
    context_object_name = 'files'

    def get_queryset(self):
        """Filter by tag if it is provided in GET parameters"""
        queryset = super(DocumentsView, self).get_queryset()
        return queryset


#@login_required(login_url='/accounts/login/')
class DocumentView(DetailView):
    model = Document
    template_name = 'document.html'
    #context_object_name = 'file'

    def get_object(self):
        return Document.objects.filter(id=self.kwargs['pk'])[0]
