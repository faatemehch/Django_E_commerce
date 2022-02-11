from django.contrib import admin
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'is_read')


admin.site.register(ContactUs, ContactUsAdmin)
