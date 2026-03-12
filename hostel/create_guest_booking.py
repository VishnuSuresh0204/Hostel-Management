import os
import django
import sys
import datetime

sys.path.append('c:/Users/VishP/Documents/python_pro/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Booking, Login, Room

try:
    riya = Login.objects.get(username='riya')
    room = Room.objects.first()
    
    # Create booking
    b = Booking.objects.create(
        user=riya,
        room=room,
        check_in=datetime.date.today(),
        check_out=datetime.date.today() + datetime.timedelta(days=2),
        total_price=100.00,
        status='PENDING'
    )
    print(f"Created Booking ID: {b.id} for User: {riya.username}")

except Exception as e:
    print(f"Error: {e}")
