from django.contrib import admin

from .models import items,products,cart,buyed, allorder
admin.site.register(items)
admin.site.register(products)
admin.site.register(cart)
admin.site.register(buyed)
admin.site.register(allorder)
