from django.db import models

class SiteSetting(models.Model):
    title = models.CharField(max_length=150)
    address = models.CharField(max_length=400)
    tel = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    about_us = models.TextField(null=True , blank=True)


    def __str__(self):
        return self.title