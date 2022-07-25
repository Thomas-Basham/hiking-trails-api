from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.forms import AdminAuthenticationForm


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username'].lower()
        user.email = self.cleaned_data['email'].lower()

        if commit:
            user.save()
        return user
    
    
# uses django's default Authentication procedure, sending email as username
# rest of function lives in backends.by
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'for': 'username'}
    ),
        label=_("Username")

    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
        }
    ))


