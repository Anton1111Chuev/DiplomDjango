from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from partsapp.models import Order, Customer


class SearchForm(forms.Form):
    query_number = forms.CharField(max_length=100,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control me-2 mx-1',
                                           'placeholder': 'Номер',
                                       }
                                   ),
                                   required=False)
    query_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control me-2 mx-1',
                                         'placeholder': 'Название',
                                     }
                                 ),
                                 required=False)

    def clean_query(self):
        query_number = self.cleaned_data['query_number']
        cleaned_query_number = " ".join(query_number.split())
        query_name = self.cleaned_data['query_name']
        if not query_name:
            query_name = ''
        return {'query_number': query_number, 'query_name': query_name}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))



class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'comment'
        )


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('phone', 'address')