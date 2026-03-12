import os
import django
import sys

sys.path.append('c:/Users/VishP/Documents/python_pro/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Booking

print("Checking Bookings with get_display_name:")
bookings = Booking.objects.all().order_by('-created_at')[:5]
for booking in bookings:
    u = booking.user
    print(f"Booking ID: {booking.id}")
    print(f"  User Type: {u.user_type}")
    print(f"  Display Name: {u.get_display_name}")
    print("-" * 20)
