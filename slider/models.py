from django.db import models
from category.models import Category
import os

def get_filename_ext(filePath):
    base_name = os.path.basename(filePath)
    name , ext = os.path.splitext(base_name)
    return name , ext

def upload_image_path(instance , filename):
    name , ext = get_filename_ext(filename)
    final_name = f"{instance.title}{ext}"
    return f"slider/{final_name}"

class Slider(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_image_path , null=True , blank=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True , blank=True)


    def __str__(self):
        return self.title
