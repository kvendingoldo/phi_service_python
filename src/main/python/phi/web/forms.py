# -*- coding: utf-8 -*-
from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ()


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    date = forms.DateField(widget=forms.SelectDateWidget)
    comments = forms.CharField(max_length=255, widget=forms.Textarea, required=False)
