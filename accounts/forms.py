from django import forms
from django.contrib.auth.models import User
from django.core import validators

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Username" , "class" : "form-control m-2"}) , label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password" , "class" : "form-control m-2"}) , label='')

    

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Username" , "class" : "form-control m-2"}) , label='' , validators=[validators.MinLengthValidator(limit_value=3 , message="Username length should be more than 2 characters")])
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email" , "class" : "form-control m-2"}) , label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Password" , "class" : "form-control m-2"}) , label='')
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "Confirm Password" , "class" : "form-control m-2"}) , label='')


    def clean_username(self):
        username = self.cleaned_data.get("username")

        users = User.objects.all()
        if username in [x.username for x in users]:
            raise forms.ValidationError("This username was token before")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        is_exist = User.objects.filter(email = email).exists()

        if is_exist:
            raise forms.ValidationError("This email was token before")

        return email
        

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 5:
            raise forms.ValidationError("Password length should be more than 5 characters")
            
        return password
    
    def clean_repassword(self):
        repassword = self.cleaned_data.get("repassword")

        if self.cleaned_data.get("password") is None:
            return repassword

        if repassword != self.cleaned_data.get("password"):
            raise forms.ValidationError("Password and Confirm Password are not same")

        return repassword