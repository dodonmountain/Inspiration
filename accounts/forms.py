from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'last_name', 'first_name', 'email')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'm-5 ',
                    }),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('last_name', 'first_name',  'email')

