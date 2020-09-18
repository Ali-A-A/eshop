from django import forms
from django.core import validators

class OrderForm(forms.Form):
    amount = forms.IntegerField(max_value=10 , min_value=1 , widget=forms.TextInput(attrs={"min" : "1" , "max" : "10" , "value" : "1"}) , validators=[validators.MaxValueValidator(10) , validators.MinValueValidator(1)])

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'product_count_item input-number'


class BillingForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "First name" , "class" : "form-control" , "id" : "first"}) , label='' , validators=[validators.MinLengthValidator(limit_value=3 , message="First length should be more than 2 characters")])
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Last name" , "class" : "form-control" , "id" : "last"}) , label='' , validators=[validators.MinLengthValidator(limit_value=3 , message="Last name length should be more than 2 characters")])
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Phone number" , "class" : "form-control" , "id" : "number"}) , label='' , validators=[validators.MinLengthValidator(limit_value=3 , message="Phone length should be more than 2 characters")])
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email" , "class" : "form-control" , "id" : "email"}) , label='')
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Address" , "class" : "form-control"}) , label='' , validators=[validators.MinLengthValidator(limit_value=3 , message="Address length should be more than 2 characters")])
    notes = forms.CharField(widget=forms.Textarea(attrs={"placeholder" : "Order Notes" , "class" : "form-control w-100"}) , label='' , validators=[validators.MinLengthValidator(limit_value=10 , message="Note length should be more than 10 characters") , validators.MaxLengthValidator(limit_value=200 , message="Note length should be less than 200 characters")] , required=False)
    is_accept_terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={"id" : "f-option4"}) , label='I\'ve read and accept the terms and conditions')