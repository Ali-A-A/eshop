from django.db import models
import os
from django.http import Http404
from django.db.models import Q
from category.models import Category

def get_filename_ext(filePath):
    base_name = os.path.basename(filePath)
    name , ext = os.path.splitext(base_name)
    return name , ext

def upload_image_path(instance , filename):
    name , ext = get_filename_ext(filename)
    final_name = f"{instance.title}{ext}"
    return f"products/{final_name}"

def upload_image_path_gallery(instance , filename):
    name , ext = get_filename_ext(filename)
    final_name = f"{instance.title}{ext}"
    return f"products_gallery/{final_name}"

class ProductManager(models.Manager):
    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    def get_product_by_id(self , id):
        qs = self.get_queryset().filter(id=id,active=True)
        if qs.exists():
            return qs[0]
        else:
            raise Http404()

    def search_by_query(self , query):
        return self.get_queryset().filter(Q(title__contains=query) | Q(description__contains=query) | Q(tag__title__contains=query) , active=True).distinct()

    def search_by_category(self , category):
        return self.get_queryset().filter(categories__title__contains=category , active=True).distinct()

class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to=upload_image_path , null=True , blank=True)
    active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category , blank=True)


    objects = ProductManager()

    def __str__(self):
        return self.title


class ProductGallery(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_image_path_gallery)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="gallery")


    def __str__(self):
        return self.title