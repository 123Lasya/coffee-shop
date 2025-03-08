from django.contrib import admin
from .models import  coffe,cartitem,orders
from .models import Profile

admin.site.register(Profile)
admin.site.register(coffe)
admin.site.register(cartitem)
admin.site.register(orders)
# Register your models here.
