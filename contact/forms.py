from django import forms
from django.core import validators

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Fullname" , "class" : "form-control"}) , label='' , validators=[validators.MinLengthValidator(limit_value=3 , message="Fullname length should be more than 2 characters")])
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email" , "class" : "form-control"}) , label='')
    subject = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Subject" , "class" : "form-control"}) , label='' , validators=[validators.MinLengthValidator(limit_value=3 , message="Subject length should be more than 2 characters")])
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder" : "Message" , "class" : "form-control w-100"}) , label='' , validators=[validators.MinLengthValidator(limit_value=10 , message="Subject length should be more than 10 characters") , validators.MaxLengthValidator(limit_value=200 , message="Subject length should be less than 200 characters")])

