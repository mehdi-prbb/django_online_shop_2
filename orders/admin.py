from django.contrib import admin

from . models import Order, OrderItem, Coupon


class OrdeItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated', 'is_paid')
    list_filter = ('is_paid', )
    inlines = (OrdeItemInline, )


admin.site.register(Coupon)