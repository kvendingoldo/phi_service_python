# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UploadFileForm, UserForm, UploadKeyForm
from .models import Document, DocumentDecryptedMeta, User, Error

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utils.cipher import AESCipher

import pickle
import codecs
import string
import random
import hashlib


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
            print(user_form.save())
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            print(hashlib.md5(aes_password.encode('utf-8')).hexdigest().strip())

            userMongo = User(name=user.get_username(), meta="todo",
                             hash=hashlib.md5(aes_password.encode('utf-8')).hexdigest().strip())
            userMongo.save()

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
                return render(request, 'error.html', {'error': Error("Your account was inactive", "")})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return render(request, 'error.html', {'error': Error("Invalid login details given", "")})
    else:
        return render(request, 'registration/login.html', {})


@login_required(login_url='/login/')
def index(request):
    files = Document.objects.all()
    return render(request, 'index.html', {'files': files})


@login_required(login_url='/login/')
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            key = form.files['key'].file.getvalue().decode("utf-8")
            if not check_key(key, request):
                render(request, 'error.html', {'error': Error("Wrong key", "The key you provided is wrong")})
            print('done')

            file = form.files['file']

            title = form.cleaned_data['title']

            meta = DocumentDecryptedMeta(title, None, form.fields['comments'])
            handle_uploaded_file(file, title, meta, key, request)
            return HttpResponseRedirect('/index')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def check_key(key, request):
    return hashlib.md5(key.encode().strip()).hexdigest() == User.objects.filter(name=request.user)[0].hash.strip()


def handle_uploaded_file(file, title, meta, key, request):
    cipher = AESCipher(key)

    pickled_file = codecs.encode(pickle.dumps(file), "base64").decode()
    file_enc = cipher.encrypt(pickled_file)

    pickled_meta = codecs.encode(pickle.dumps(meta), "base64").decode()
    meta_enc = cipher.encrypt(pickled_meta)

    document = Document(meta=meta_enc, title=title, body=file_enc, owner=request.user)
    document.save()


class DocumentsView(LoginRequiredMixin, ListView):
    model = Document

    login_url = '/login/'
    template_name = 'index.html'
    context_object_name = 'files'

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)


def generate_decoded_form(key, doc):
    cipher = AESCipher(key)

    body = pickle.loads(codecs.decode(cipher.decrypt(bytes(doc.body, encoding="utf-8")[2:-1].decode()).encode(), "base64"))
    meta = pickle.loads(codecs.decode(cipher.decrypt(bytes(doc.body, encoding="utf-8")[2:-1].decode()).encode(), "base64"))

    return {"form": {
        'title': doc.title,
        'meta': meta,
        'body': body
    }}


@login_required(login_url='/login/')
def document_view(request, pk):
    if request.method == 'POST':
        form = UploadKeyForm(request.POST, request.FILES)
        if form.is_valid():
            key = form.files['key'].file.getvalue().decode("utf-8")
            if not check_key(key, request):
                render(request, 'error.html', {'error': Error("Wrong key", "The key you provided is wrong")})

            return render(request, 'document.html',
                          generate_decoded_form(key, Document.objects.filter(_id=pk)[0]))
    else:
        form = UploadKeyForm()
    return render(request, 'security_page.html', {'form': form})
