from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom User Model
class Login(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'), # Resident
        ('guest', 'Guest'), # Visitor
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    view_password = models.CharField(max_length=100, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def get_display_name(self):
        if self.user_type == 'user':
            try:
                return self.resident.name
            except:
                return self.username
        elif self.user_type == 'guest':
            try:
                return self.guest.name
            except:
                return self.username
        return self.username

# Resident Profile
class Resident(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='resident')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

# Guest Profile
class Guest(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='guest')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    identity_proof = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Room Model
class Room(models.Model):
    RENTAL_CHOICES = [
        ('DAILY', 'Daily'),
        ('MONTHLY', 'Monthly'),
    ]
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    rental_type = models.CharField(max_length=10, choices=RENTAL_CHOICES, default='MONTHLY')
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return f"Room {self.number} ({self.rental_type})"

# Mess Menu
class MessMenu(models.Model):
    DAYS = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    day_of_week = models.CharField(max_length=3, choices=DAYS, unique=True)
    breakfast = models.CharField(max_length=200)
    lunch = models.CharField(max_length=200)
    dinner = models.CharField(max_length=200)

    def __str__(self):
        return self.get_day_of_week_display()

# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
    ]

    # Link to the main User model (Login) so both Residents and Guests can book
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"

# Feedback Model
class Feedback(models.Model):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('GUEST', 'Guest'),
    ]

    user = models.ForeignKey(Login, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    role_type = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"Feedback from {self.user.get_display_name if self.user else 'Guest'}"




# Event Model
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Leave Request Model
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='leave_requests')
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave for {self.resident.name} ({self.status})"

# Fee Model
class Fee(models.Model):
    FEE_TYPE_CHOICES = [
        ('ROOM', 'Room Fee'),
        ('MESS', 'Mess Fee'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    ]
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_type = models.CharField(max_length=10, choices=FEE_TYPE_CHOICES)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)


# Attendance Model
class Attendance(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, default='PRESENT')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resident', 'date')

    def __str__(self):
        return f"{self.resident.name} - {self.date}"
