from django import forms
from .models import Product, Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description','price','quantity']
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text="Insira um email valido ")

    class Meta:
        model = Account
        fields = ['email','username', 'cpf', 'password1','password2']

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ['email','password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Login Invalido")
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username']
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" ja esta em uso' % email )
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" ja esta em uso' % username )
