import os
import django
import sys

sys.path.append('c:/Users/VishP/Documents/python_pro/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Login

try:
    riya = Login.objects.get(username='riya')
    print(f"User: {riya.username}")
    print(f"Type: {riya.user_type}")
    if hasattr(riya, 'guest'):
        print(f"Guest Profile Name: {riya.guest.name}")
    else:
        print("NO GUEST PROFILE LINKED")
except Exception as e:
    print(f"Error: {e}")
