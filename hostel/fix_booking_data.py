import os
import django
import sys

# Setup Django environment
sys.path.append('c:/Users/VishP/Documents/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Booking, Login

try:
    booking = Booking.objects.get(id=1)
    rahul = Login.objects.get(id=2)
    booking.user = rahul
    booking.save()
    print("Successfully updated Booking 1 to belong to Rahul.")
except Exception as e:
    print(f"Error: {e}")
