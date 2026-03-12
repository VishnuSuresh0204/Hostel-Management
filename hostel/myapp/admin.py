from django.contrib import admin
from .models import Login, Resident, Guest, Room, MessMenu, Booking, Feedback

admin.site.register(Login)
admin.site.register(Resident)
admin.site.register(Guest)
admin.site.register(Room)
admin.site.register(MessMenu)
admin.site.register(Booking)
admin.site.register(Feedback)
