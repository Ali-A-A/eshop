from django.shortcuts import render
from .forms import ContactForm
from .models import Contact
from django.shortcuts import redirect
from site_setting.models import SiteSetting

def contact_page(reqeust):
    contact_form = ContactForm(reqeust.POST or None)
    site_setting = SiteSetting.objects.get(id=1)
    context = {
        "contact_form" : contact_form,
        "site_setting" : site_setting
    }
    if contact_form.is_valid():
        text = contact_form.cleaned_data.get("text")
        name = contact_form.cleaned_data.get("name")
        subject = contact_form.cleaned_data.get("subject")
        email = contact_form.cleaned_data.get("email")
        contact = Contact(email=email , text=text , full_name=name , subject=subject)
        contact.save()
        return redirect('/?message=Your+message+sent+successfully')
    return render(reqeust , 'contact/contact_page.html' , context)

