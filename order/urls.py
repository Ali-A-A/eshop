from django.urls import path
from .views import user_order , cart_view , delete_view , checkout_view , confirm_view

app_name='order'
urlpatterns = [
    path('' , user_order , name='user_order'),
    path('cart' , cart_view , name='card_view'),
    path('delete' , delete_view , name='delete'),
    path('confirm/' , confirm_view , name='confirm'),
    path('checkout' , checkout_view , name='checkout'),
    # path('request/', send_request, name='request'),
    # path('verify/<int:id>', verify , name='verify'),
]
