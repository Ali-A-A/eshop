from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'is_read']
    list_filter = ['is_read']
    list_editable = ['is_read']

admin.site.register(Contact , ContactAdmin)