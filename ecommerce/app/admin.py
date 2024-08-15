from django.contrib import admin
from .models import CustomUser, Category, SubCategory, Slider, Product,Address, Order, OrderItem,City,Advertisment
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'mobilenumber', 'is_staff', 'is_active',)
    list_filter = ('email', 'name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'mobilenumber',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobilenumber', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'subcategory_count', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'product_count', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name')
    list_filter = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price', 'discounted_price', 'stock', 'featured', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name', 'subcategory__name')
    list_filter = ('category', 'subcategory', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('price', 'stock', 'featured')

class SliderAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(City)
admin.site.register(Advertisment)
