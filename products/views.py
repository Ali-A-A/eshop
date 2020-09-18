from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product
from django.db.models import Q
from category.models import Category
from order.forms import OrderForm


class ProductsList(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args , **kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        request = self.request
        if request.GET.get('category') is not None and len(request.GET.get('category')) > 0:
            print(request.GET.get('category'))
            return Product.objects.search_by_category(request.GET.get('category'))
        elif request.GET.get('search') is not None and len(request.GET.get('search')) > 0:
            return Product.objects.search_by_query(request.GET.get('search'))
        else:
            return Product.objects.get_active_products()

def product_detail(request , id):
    product = Product.objects.get_product_by_id(id)
    order_form = OrderForm()
    context = {
        "object" : product,
        "order_form" : order_form
    }
    return render(request , 'products/products_detail.html' , context)
