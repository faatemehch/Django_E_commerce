from django.db import models


class ContactUs( models.Model ):
    fullname = models.CharField( max_length=200 )
    email = models.EmailField()
    subject = models.CharField( max_length=300 )
    message_text = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True )
    is_read = models.BooleanField( default=False, null=True )
    read_at = models.DateTimeField( auto_now=True )
    response = models.TextField()

    def __str__(self):
        return self.fullname
