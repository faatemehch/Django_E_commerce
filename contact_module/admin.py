from django.contrib import admin
from utils.email_services import EmailService
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'is_read')

    def save_model(self, request, obj, form, change):
        if change:
            EmailService.send_email(subject='response message', to=obj.email, context={'response': obj.response, 'user_message':obj.message_text},
                                    template_name='emails/response_contact_us_email.html')
        return super().save_model(request, obj, form, change)


admin.site.register(ContactUs, ContactUsAdmin)
