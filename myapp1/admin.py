from django.contrib import admin
from .models import Room, Booking

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'teacher', 'is_active')  # Display relevant fields in the list
    search_fields = ('name', 'teacher__username')  # Allow search by room name and teacher's username
    list_filter = ('is_active', 'teacher')  # Add filters for active status and teacher

class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'date', 'booked_by')  # Display room, user, date, and who booked the room
    list_filter = ('room', 'user', 'date')  # Add filters for room, user, and date
    search_fields = ('room__name', 'user__username')  # Allow search by room name and user

# Register the models with custom admin classes
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
