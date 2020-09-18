from django.db import models

class Contact(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return self.subject