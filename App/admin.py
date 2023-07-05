from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','price','category','image']
    list_filter = ['category']

class ProductInline(admin.TabularInline):
    model = Product
    fields = ('product_name', 'price', 'image')
    extra = 0
    readonly_fields = ('product_name', 'price','image')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'total_products')
    inlines = [ProductInline]

    def total_products(self, obj):
        return obj.products.count()
    total_products.short_description = 'Total Products'

@admin.register(CartItems)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','price','quantity','total_price']

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','full_name','email','phone','payment_status']

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['id','name','subject','email','message']

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id','name','phone','email','password']

@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','product_name','reviews','rating']