from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Words, Sentence


class SignUpForm(UserCreationForm):
    username = forms.CharField(label = 'username', \
        widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    password1 = forms.CharField(label = 'Password', \
        widget = forms.PasswordInput(attrs = {'class' : 'form-control'})
        )
    password2 = forms.CharField(label = 'Password', \
        widget = forms.PasswordInput(attrs = {'class' : 'form-control'})
        )

class SignInForm(AuthenticationForm):
    username = forms.CharField(label = 'username', \
        widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    password = forms.CharField(label = 'password', \
        widget = forms.PasswordInput(attrs = {'class' : 'form-control'})
        )

class CreateForm(forms.Form):
    word = forms.CharField(label = '英単語', \
        widget = forms.TextInput(attrs = {'class' : 'form-control'}))

class Create_myselfForm(forms.Form):
    word = forms.CharField(label = '英単語', \
        widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    meaning = forms.CharField(label = '意味', \
        widget = forms.TextInput(attrs = {'class' : 'form-control'}))
        
class EditForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = ['meaning']

class CountForm(forms.Form):
    sentence = forms.CharField(label = '英文', \
        widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    class Meta:
        model = Sentence
        field = ['sentence']

class TwitterForm(forms.Form):
    screen_name = forms.CharField(label = 'ユーザー名', \
        widget = forms.TextInput(attrs = {'class' : 'form-control'}))