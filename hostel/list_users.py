import os
import django
import sys

sys.path.append('c:/Users/VishP/Documents/python_pro/hostel/hostel/hostel')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel.settings')
django.setup()

from myapp.models import Login

print("Listing Users:")
for u in Login.objects.all():
    print(f"User: {u.username}, Type: {u.user_type}")
