import os
import django
import sys

# Setup Django environment
sys.path.append('c:/Users/VishP/Documents/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Booking, Login

print(f"{'Booking ID':<10} | {'Username':<15} | {'User Type':<10} | {'Resident Name':<20} | {'Guest Name':<20}")
print("-" * 80)

for booking in Booking.objects.all():
    user = booking.user
    resident_name = "N/A"
    guest_name = "N/A"
    
    if hasattr(user, 'resident'):
        resident_name = user.resident.name
    if hasattr(user, 'guest'):
        guest_name = user.guest.name
        
    print(f"{booking.id:<10} | {user.username:<15} | {user.user_type:<10} | {resident_name:<20} | {guest_name:<20}")

print("\n" + "="*80 + "\nAll Users:\n")
print(f"{'ID':<5} | {'Username':<15} | {'Type':<10} | {'Name':<20}")
for u in Login.objects.all():
    name = "N/A"
    if hasattr(u, 'resident'): name = u.resident.name
    elif hasattr(u, 'guest'): name = u.guest.name
    print(f"{u.id:<5} | {u.username:<15} | {u.user_type:<10} | {name:<20}")
