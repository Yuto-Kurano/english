from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Words


class SignUpForm(UserCreationForm):
    username = forms.CharField(label = 'username', \
        widget = forms.TextInput(attrs = {'class' : 'form control'}))
    password1 = forms.CharField(label = 'Password', \
        widget = forms.PasswordInput(attrs = {'class' : 'form control'})
        )
    password2 = forms.CharField(label = 'Password', \
        widget = forms.PasswordInput(attrs = {'class' : 'form control'})
        )

class SignInForm(AuthenticationForm):
    username = forms.CharField(label = 'username', \
        widget = forms.TextInput(attrs = {'class' : 'form control'}))
    password = forms.CharField(label = 'password', \
        widget = forms.PasswordInput(attrs = {'class' : 'form control'})
        )

class CreateForm(forms.Form):
    word = forms.CharField(label = 'word', \
        widget = forms.TextInput(attrs = {'class' : 'form control'}))
        
class EditForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = ['meaning']