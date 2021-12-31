from django.db import models


class Slider( models.Model ):
    title = models.CharField( max_length=200 )
    image = models.ImageField( upload_to='slider_images/' )

    class Meta:
        verbose_name = 'slider image'
        verbose_name_plural = 'Slider Images'

    def __str__(self):
        return self.title
