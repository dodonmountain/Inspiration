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
        label = False

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3 text-small',
        'placeholder': '사용자 이름'
        }), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-5 text-small',
        'placeholder': '비밀번호'
        }), label='')
    class Meta:
        model = get_user_model()
        fields = ('username','password')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('last_name', 'first_name',  'email')

