from django.contrib import admin
from .models import Customer , Cake , CakeCustomization , Cart  , Order ,Store

# Register your models here.

admin.site.register(Customer)
admin.site.register(Cake)
admin.site.register(CakeCustomization)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Store)



