from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Task

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          "class": "form-control"}),
    )


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'