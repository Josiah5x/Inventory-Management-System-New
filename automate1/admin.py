from django.contrib import admin
from .models import OrderDocument, OrderItem,Vat, CreditFacility, Currency, Supplier, Product

# Register your models here.
admin.site.register(OrderDocument)
admin.site.register(OrderItem)
admin.site.register(Vat)
admin.site.register(Currency)
admin.site.register(CreditFacility)
admin.site.register(Supplier)
admin.site.register(Product)