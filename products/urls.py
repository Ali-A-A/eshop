from django.urls import path
from .views import ProductsList , product_detail

app_name = 'products'
urlpatterns = [
    path('list' , ProductsList.as_view() , name='list'),
    path('detail/<int:id>' , product_detail , name='detail'),
]
