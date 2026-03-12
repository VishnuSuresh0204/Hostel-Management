import os
import django
import sys

sys.path.append('c:/Users/VishP/Documents/python_pro/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Booking

print("Checking Guest Bookings:")
guest_bookings = Booking.objects.filter(user__user_type='guest')
if not guest_bookings.exists():
    print("No guest bookings found.")
else:
    for booking in guest_bookings:
        u = booking.user
        print(f"Booking ID: {booking.id}")
        print(f"  User: {u.username}")
        print(f"  User Type: '{u.user_type}'")
        try:
            print(f"  Guest Name: {u.guest.name}")
        except Exception as e:
            print(f"  Guest Access Error: {e}")
        print("-" * 20)
