from django.contrib import admin
from .models import SerialKey, Subscription

@admin.register(SerialKey)
class SerialKeyAdmin(admin.ModelAdmin):
    list_display = ('serial_key',)
    search_fields = ('serial_key',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('serial_key', 'start_date', 'end_date', 'last_checkin')  # Added last_checkin field
    search_fields = ('serial_key__serial_key',)  # Allows searching by the serial key
    list_filter = ('start_date', 'end_date', 'last_checkin')  # Added last_checkin to filter options

