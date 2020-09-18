from django.shortcuts import render , redirect , reverse , get_object_or_404 , Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import OrderForm , BillingForm
from .models import OrderRow , Order , Billing
from products.models import Product
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from datetime import datetime

# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Toman / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.

# def send_request(request):
#     total = 0
#     order : Order = Order.objects.filter(user__id=request.user.id , is_paid=False).first()
#     if order is not None:
#         total = order.get_total_price()
#         result = client.service.PaymentRequest(MERCHANT, total, description, email, mobile, f'{CallbackURL}{order.id}')
#         if result.Status == 100:
#             return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
#         else:
#             return HttpResponse('Error code: ' + str(result.Status))

#     raise Http404("Order Not Found")

# def verify(request , id):
#     if request.GET.get('Status') == 'OK':
#         result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
#         if result.Status == 100:
#             order : Order = Order.objects.get(id=id)
#             order.is_paid = True
#             order.payment_date = time.time()
#             order.save()
#             return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
#         elif result.Status == 101:
#             return HttpResponse('Transaction submitted : ' + str(result.Status))
#         else:
#             return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
#     else:
#         return HttpResponse('Transaction failed or canceled by user')

@login_required
def user_order(request):
    if request.method == "GET":
        print("HI")
        return redirect('/')
    order_form = OrderForm(request.POST)
    context = {
        "order_form" : order_form
    }
    if order_form.is_valid():
        order = Order.objects.filter(user__id=request.user.id , is_paid=False).first()
        if order is None:
            order = Order(user=request.user)
            order.save()
        product_id = request.POST.get("product_id")
        amount = order_form.cleaned_data.get("amount")
        product = get_object_or_404(Product , pk=product_id)
        order_row = OrderRow(order=order , product=product , price=product.price * amount , amount=amount)
        order_row.save()
        return redirect(reverse("order:card_view"))
    return redirect(reverse('products:detail' , kwargs={"id" : request.POST.get("product_id")}))


@login_required
def cart_view(request):
    order = Order.objects.filter(user__id=request.user.id , is_paid=False).first()
    context = {}
    print(order)
    if order is not None:
        context = {"order":order}
    return render(request , 'order/cart.html' , context)


@login_required
def delete_view(request):
    if request.method == "GET":
        return redirect('/')
    OrderRow.objects.filter(product__id=request.POST.get("product_id"),order__user__id=request.user.id).delete()
    order = Order.objects.filter(user__id=request.user.id , is_paid=False).first()
    if order is not None:
        if not order.order_row.exists():
            order.delete()
    return redirect(reverse('order:card_view'))

@login_required
def checkout_view(request):
    order : Order = Order.objects.filter(user__id=request.user.id , is_paid=False).first()
    context = {}
    if order is not None:
        form = BillingForm(request.POST or None)
        total = order.get_total_price()
        context = {"order":order , "total" : total , "form" : form}
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            notes = form.cleaned_data.get("notes")
            phone = form.cleaned_data.get("phone")
            Billing.objects.create(order=order , user=request.user , first_name=first_name , last_name=last_name , email=email , address=address , notes=notes , phone=phone)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!assume that transaction was successful !!!!!!!!!!!!!!!!!!!!!!!!!!
            order.is_paid = True
            order.payment_date = datetime.now()
            order.save()
            return redirect(f"/order/confirm/?id={order.id}")
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
    return render(request , 'order/checkout.html' , context)


@login_required
def confirm_view(request):
    order : Order = Order.objects.filter(id=request.GET.get("id")).first()
    billing : Billing = Billing.objects.filter(user=request.user,order__id=request.GET.get("id")).first()
    if order is None or billing is None:
        return redirect("/")
    context = {
        "price" : order.get_total_price(),
        "date" : order.payment_date,
        "billing" : billing,
        "order" : order
    }
    return render(request , 'order/confirmation.html' , context)

