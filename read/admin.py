from django.contrib import admin
from . models import *

class AdminProduct(admin.ModelAdmin):
        list_display = ['name' , 'category']
        
class AdminCategory(admin.ModelAdmin):
        list_display = ['name']

admin.site.register(Registration)
admin.site.register(Joining)
admin.site.register(Requests)
admin.site.register(Product , AdminProduct)
admin.site.register(Category , AdminCategory)
admin.site.register(Order)
