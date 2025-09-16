from django.contrib import admin
from .models import Order, Item

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total','created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('order','movie','price','quantity')
