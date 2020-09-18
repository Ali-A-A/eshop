from django.contrib import admin
from .models import Order , OrderRow , Billing

admin.site.register(Order)
admin.site.register(OrderRow)
admin.site.register(Billing)
