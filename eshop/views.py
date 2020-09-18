from django.shortcuts import render , redirect
from slider.models import Slider
from site_setting.models import SiteSetting
from order.models import Order , Billing
from django.contrib.auth.decorators import login_required


def header(request):
    if request.user:
        order = Order.objects.filter(user__id=request.user.id,is_paid=False).first()
    context = {
        'title' : 'Title',
        'order' : order
    }
    return render(request , 'shared/Header.html' , context)

def footer(reqeust):
    site_setting = SiteSetting.objects.get(id=1)
    context = {
        "about" : "Developed by Ali",
        "site_setting" : site_setting
    }
    return render(reqeust , 'shared/Footer.html' , context)


def home_page(request):
    message = request.GET.get("message")
    sliders = Slider.objects.all()
    context = {
        "sliders" : sliders,
        "message" : message
    }
    return render(request , 'home_page.html' , context)


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    billings = Billing.objects.filter(user=request.user)
    context = {
        "orders" : orders,
        "billings" : billings
    }
    return render(request , 'shared/profile.html' , context)

