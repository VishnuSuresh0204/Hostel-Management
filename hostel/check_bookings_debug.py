import os
import django
import sys

# Setup Django environment
sys.path.append('c:/Users/VishP/Documents/python_pro/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Booking, Login, Guest, Resident

print("Checking Bookings:")
bookings = Booking.objects.all().order_by('-created_at')[:5]
for booking in bookings:
    u = booking.user
    print(f"Booking ID: {booking.id}")
    print(f"  User: {u.username} (ID: {u.id})")
    print(f"  User Type: '{u.user_type}'")
    
    # Check manual relation access
    has_guest = hasattr(u, 'guest')
    has_resident = hasattr(u, 'resident')
    print(f"  Has Guest attr: {has_guest}")
    print(f"  Has Resident attr: {has_resident}")
    
    if has_guest:
        try:
            print(f"  Guest Name: {u.guest.name}")
        except Exception as e:
            print(f"  Guest Access Error: {e}")
            
    if has_resident:
         try:
            print(f"  Resident Name: {u.resident.name}")
         except Exception as e:
            print(f"  Resident Access Error: {e}")
            
    print("-" * 20)
