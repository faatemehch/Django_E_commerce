from django.db import models


class Slider(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='slider_images/')

    class Meta:
        verbose_name = 'slider image'
        verbose_name_plural = 'Slider Images'

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    fax = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return str(self.pk)
