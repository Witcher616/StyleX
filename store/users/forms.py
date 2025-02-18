import uuid
from datetime import timedelta

from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User, EmailVerification
from django.utils.timezone import now
from django import forms

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введите имя пользователя"}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль' }))
    
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control py-4', 'placeholder': "Введите имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control py-4', 'placeholder': "Введите фамилию"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control py-4', 'placeholder': "Введите имя пользователя"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
            'class': 'form-control py-4', 'placeholder': "Введите адрес эл. почты"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4', 'placeholder': "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4', 'placeholder': "Подтвердите пароль"}))
    
    def save(self, commit=True) :
        user = super(UserRegistrForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user
        
        
class UserProfileForm(UserChangeForm):
        class Meta:
                model = User
                fields = ('first_name', 'last_name', 'image', 'username', 'email')
        
        first_name = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control py-4', }))
        last_name = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control py-4', }))
        image = forms.ImageField(widget=forms.FileInput(attrs={
                'class': 'custom-file-input'}), required=False )
        username = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control py-4'}))
        email = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control py-4', 'readonly': True}))
        