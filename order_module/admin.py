from django.contrib import admin

from . import models


class OrderAdmin( admin.ModelAdmin ):
    list_display = ('__str__', 'is_paid', 'is_send', 'payment_date')


class ProvinceTabularCity( admin.TabularInline ):
    model = models.City


class ProvinceAdmin( admin.ModelAdmin ):
    inlines = [ProvinceTabularCity]


admin.site.register( models.Order, OrderAdmin )
admin.site.register( models.OrderDetail )
admin.site.register( models.Coupon )
admin.site.register( models.Province, ProvinceAdmin )
admin.site.register( models.City )
