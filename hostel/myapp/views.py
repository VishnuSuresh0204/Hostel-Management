from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
from django.contrib import messages
import datetime

# Auth Views
def register_resident(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Additional fields
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        roll_number = request.POST.get('roll_number')

        if not Login.objects.filter(username=username).exists():
            user = Login.objects.create_user(username=username, email=email, password=password, user_type='user', view_password=password)
            user.save()
            Resident.objects.create(login=user, name=name, email=email, phone=phone, address=address, roll_number=roll_number)
            return redirect('/login/')
        else:
            msg = "Username already exists"
    return render(request, 'register_resident.html', {'msg': msg})

def register_guest(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Additional fields
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        identity_proof = request.POST.get('identity_proof')

        if not Login.objects.filter(username=username).exists():
            user = Login.objects.create_user(username=username, email=email, password=password, user_type='guest', view_password=password)
            user.save()
            Guest.objects.create(login=user, name=name, email=email, phone=phone, address=address, identity_proof=identity_proof)
            return redirect('/login/')
        else:
            msg = "Username already exists"
    return render(request, 'register_guest.html', {'msg': msg})

def login_view(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.user_type == 'guest':
                try:
                    guest = Guest.objects.get(login=user)
                    login(request, user)
                    request.session['guest_id'] = guest.id
                    return redirect('/guest_home/')
                except Guest.DoesNotExist:
                     msg = "Guest profile not found"

            elif user.user_type == 'user':
                try:
                    resident = Resident.objects.get(login=user)
                    login(request, user)
                    request.session['resident_id'] = resident.id
                    return redirect('/user_home/')
                except Resident.DoesNotExist:
                    msg = "Resident profile not found"
            
            elif user.user_type == 'admin':
                login(request, user)
                return redirect('/admin_home/')
        else:
            msg = "Invalid credentials"
    return render(request, 'login.html', {'msg': msg})

def auth_logout(request):
    logout(request)
    request.session.flush()
    return redirect('/')

# General Views
def index(request):
    return render(request, 'index.html')

def user_index(request):
    if 'resident_id' in request.session:
        return render(request, 'USER/index.html')
    return redirect('/login/')

def guest_index(request):
    if 'guest_id' in request.session:
        return render(request, 'GUEST/index.html')
    return redirect('/login/')

def admin_index(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        return render(request, 'ADMIN/index.html')
    return redirect('/login/')

# Admin Functions
def view_rooms(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        rooms = Room.objects.all()
        
        # Attach occupant info
        # Attach occupant info
        # Attach occupant info
        for room in rooms:
            room.occupants_list = []
            
            # Find the active bookings for this room
            active_bookings = Booking.objects.filter(
                room=room,
                status__in=['PENDING', 'APPROVED', 'CONFIRMED'],
                check_out__gte=datetime.date.today()
            )
            
            for booking in active_bookings:
                room.occupants_list.append(booking.user.get_display_name)

        return render(request, 'ADMIN/view_rooms.html', {'rooms': rooms})
    return redirect('/login/')

def add_room(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            number = request.POST.get('number')
            capacity = request.POST.get('capacity')
            price = request.POST.get('price')
            rental_type = request.POST.get('rental_type')
            image = request.FILES.get('image')
            
            Room.objects.create(
                number=number,
                capacity=capacity,
                price=price,
                rental_type=rental_type,
                image=image,
                status='AVAILABLE'
            )
            return redirect('/view_rooms/')
        return render(request, 'ADMIN/add_room.html')
    return redirect('/login/')

def edit_room(request, id):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        try:
            room = Room.objects.get(id=id)
            if request.method == 'POST':
                room.number = request.POST.get('number')
                room.capacity = request.POST.get('capacity')
                room.price = request.POST.get('price')
                room.rental_type = request.POST.get('rental_type')
                
                if request.FILES.get('image'):
                    room.image = request.FILES.get('image')
                
                room.save()
                return redirect('/view_rooms/')
            return render(request, 'ADMIN/edit_room.html', {'room': room})
        except Room.DoesNotExist:
            return redirect('/view_rooms/')
    return redirect('/login/')

def delete_room(request, id):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        try:
            room = Room.objects.get(id=id)
            room.delete()
        except Room.DoesNotExist:
            pass
        return redirect('/view_rooms/')
    return redirect('/login/')

def manage_mess(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            day_of_week = request.POST.get('day_of_week')
            breakfast = request.POST.get('breakfast')
            lunch = request.POST.get('lunch')
            dinner = request.POST.get('dinner')
            
            MessMenu.objects.update_or_create(
                day_of_week=day_of_week,
                defaults={
                    'breakfast': breakfast,
                    'lunch': lunch,
                    'dinner': dinner
                }
            )
            return redirect('/manage_mess/')

        menu = MessMenu.objects.all()
        # Custom sort to ensure Mon-Sun order
        days_order = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        menu = sorted(menu, key=lambda x: days_order.index(x.day_of_week) if x.day_of_week in days_order else 7)
        
        return render(request, 'ADMIN/manage_mess.html', {'menu': menu})
    return redirect('/login/')

def view_bookings_admin(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        bookings = Booking.objects.all().order_by('-created_at')
        return render(request, 'ADMIN/view_bookings.html', {'bookings': bookings})
    return redirect('/login/')

def view_feedback_admin(request):
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        return redirect('/login/')

    feedbacks = (
        Feedback.objects
        .select_related('user')
        .order_by('-date')
    )

    return render(
        request,
        'ADMIN/view_feedback.html',
        {'feedbacks': feedbacks}
    )

# New Admin Features
def update_room_status(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            room_id = request.POST.get('room_id')
            status = request.POST.get('status')
            room = Room.objects.get(id=room_id)
            room.status = status
            room.save()
            return redirect('/view_rooms/')
        return redirect('/view_rooms/')
    return redirect('/login/')

def approve_booking(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            booking = Booking.objects.get(id=booking_id)
            booking.status = 'APPROVED' # Wait for user payment
            booking.save()
            # Room remains OCCUPIED (Reserved)
        return redirect('/view_bookings_admin/')
    return redirect('/login/')

def reject_booking(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            booking = Booking.objects.get(id=booking_id)
            
            # If rejected, free the room
            room = booking.room
            room.status = 'AVAILABLE'
            room.save()
            
            booking.status = 'CANCELLED'
            booking.save()
        return redirect('/view_bookings_admin/')
    return redirect('/login/')

def confirm_payment(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    if request.method == 'POST':
        # Processing Payment from Payment Page Form
        payment_type = request.POST.get('type')
        item_id = request.POST.get('id')
        
        if payment_type == 'booking':
            try:
                booking = Booking.objects.get(id=item_id)
                booking.payment_status = 'PAID'
                booking.status = 'CONFIRMED'
                booking.save()
                messages.success(request, "Payment successful! Booking confirmed.")
                
                if booking.user.user_type == 'user':
                    return redirect('/my_bookings/')
                else:
                    return redirect('/guest_bookings/')
            except Booking.DoesNotExist:
                 messages.error(request, "Booking not found.")
                 return redirect('/')
                 
        elif payment_type == 'fee': 
            try:
                fee = Fee.objects.get(id=item_id)
                fee.status = 'PAID'
                fee.save()
                messages.success(request, "Fee paid successfully!")
                return redirect('/view_fees_user/')
            except Fee.DoesNotExist:
                messages.error(request, "Fee record not found.")
                return redirect('/view_fees_user/')

    else:
        # GET request - Show Payment Page
        payment_type = request.GET.get('type')
        item_id = request.GET.get('id')
        
        context = {
            'type': payment_type,
            'id': item_id,
            'amount': 0
        }
        
        if payment_type == 'booking':
            try:
                booking = Booking.objects.get(id=item_id)
                context['amount'] = booking.total_price
            except Booking.DoesNotExist:
                messages.error(request, "Invalid booking.")
                return redirect('/')
        elif payment_type == 'fee':
             try:
                fee = Fee.objects.get(id=item_id)
                context['amount'] = fee.amount
             except Fee.DoesNotExist:
                messages.error(request, "Invalid fee.")
                return redirect('/view_fees_user/')
                
        return render(request, 'payment.html', context)

def view_users(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        users = Resident.objects.all()
        return render(request, 'ADMIN/view_users.html', {'users': users})
    return redirect('/login/')

def block_user(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            login_obj = Login.objects.get(id=user_id)
            login_obj.is_blocked = True
            login_obj.save()
        return redirect('/view_users/')
    return redirect('/login/')

def unblock_user(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            login_obj = Login.objects.get(id=user_id)
            login_obj.is_blocked = False
            login_obj.save()
        return redirect('/view_users/')
    return redirect('/login/')

def view_guests(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        guests = Guest.objects.all()
        return render(request, 'ADMIN/view_guests.html', {'guests': guests})
    return redirect('/login/')

def manage_events(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            date = request.POST.get('date')
            time = request.POST.get('time')
            venue = request.POST.get('venue')
            Event.objects.create(title=title, description=description, date=date, time=time, venue=venue)
            return redirect('/manage_events/')
        events = Event.objects.all().order_by('-date')
        return render(request, 'ADMIN/manage_events.html', {'events': events})
    return redirect('/login/')

def delete_event(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            event_id = request.POST.get('event_id')
            Event.objects.get(id=event_id).delete()
        return redirect('/manage_events/')
    return redirect('/login/')

def view_leave_requests(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        leaves = LeaveRequest.objects.all().order_by('-created_at')
        return render(request, 'ADMIN/view_leave_requests.html', {'leaves': leaves})
    return redirect('/login/')

def approve_leave(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            leave_id = request.POST.get('leave_id')
            leave = LeaveRequest.objects.get(id=leave_id)
            leave.status = 'APPROVED'
            leave.save()
        return redirect('/view_leave_requests/')
    return redirect('/login/')

def reject_leave(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            leave_id = request.POST.get('leave_id')
            leave = LeaveRequest.objects.get(id=leave_id)
            leave.status = 'REJECTED'
            leave.save()
        return redirect('/view_leave_requests/')
    return redirect('/login/')

def manage_fees(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        fees = Fee.objects.all().order_by('-created_at')
        users = Login.objects.exclude(user_type='admin')
        return render(request, 'ADMIN/manage_fees.html', {'fees': fees, 'users': users})
    return redirect('/login/')

def add_fee(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            amount = request.POST.get('amount')
            fee_type = request.POST.get('fee_type')
            due_date = request.POST.get('due_date')
            user = Login.objects.get(id=user_id)
            Fee.objects.create(user=user, amount=amount, fee_type=fee_type, due_date=due_date)
            return redirect('/manage_fees/')
    return redirect('/login/')

def mark_fee_paid(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        if request.method == 'POST':
            fee_id = request.POST.get('fee_id')
            fee = Fee.objects.get(id=fee_id)
            fee.status = 'PAID'
            fee.save()
        return redirect('/manage_fees/')
    return redirect('/login/')

# User Functions (Resident)
def view_mess_user(request):
    if 'resident_id' in request.session:
        menu = MessMenu.objects.all()
        return render(request, 'USER/view_mess.html', {'menu': menu})
    return redirect('/login/')

def book_room(request):
    # Filter rooms based on user type
    rooms = Room.objects.filter(status='AVAILABLE')
    
    if 'resident_id' in request.session:
        # Residents only see MONTHLY rooms
        rooms = rooms.filter(rental_type='MONTHLY')
    elif 'guest_id' in request.session:
        # Guests only see DAILY rooms
        rooms = rooms.filter(rental_type='DAILY')
    else:
        return redirect('/login/')

    template = 'USER/book_room.html'
    if 'guest_id' in request.session:
        template = 'GUEST/book_room.html'
    
    return render(request, template, {'rooms': rooms})

def place_booking(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        user_id = None
        user_type = None

        if 'resident_id' in request.session:
            user_id = request.session['resident_id']
            user_type = 'user'
        elif 'guest_id' in request.session:
            user_id = request.session['guest_id']
            user_type = 'guest'
        else:
            return redirect('/login/')
            
        try:
            room = Room.objects.get(id=room_id)
            if user_type == 'user':
                resident = Resident.objects.get(id=user_id)
                user = resident.login
            else: # guest
                guest = Guest.objects.get(id=user_id)
                user = guest.login
            
            # Check for existing active booking
            active_booking = Booking.objects.filter(
                user=user,
                status__in=['PENDING', 'APPROVED', 'CONFIRMED'],
                check_out__gte=datetime.date.today()
            ).exists()
            
            if active_booking:
                messages.error(request, "You already have an active or pending booking. You cannot book another room until your current booking ends.")
                return redirect('/book_room/')

            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')

            # Date Validation
            d1 = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
            d2 = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
            delta = (d2 - d1).days

            if delta <= 0:
                 messages.error(request, "Invalid Dates. Check-out must be after check-in.")
                 return redirect('/book_room/')

            if user_type == 'user':
                if delta < 20:
                    messages.error(request, "Residents must book for at least 20 days.")
                    return redirect('/book_room/')
            elif user_type == 'guest':
                if delta > 7:
                    messages.error(request, "Guests can only book for up to 7 days.")
                    return redirect('/book_room/')
            
            # Simple price calculation
            total_price = room.price * delta if room.rental_type == 'DAILY' else room.price # Monthly fixed or per day? Assuming monthly fixed for now or logic to be refined.
            
            Booking.objects.create(
                user=user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                total_price=total_price,
                payment_status='UNPAID', # Wait for payment
                status='PENDING' # Wait for Approval
            )
            
            # Update room status to prevent double booking
            room.status = 'OCCUPIED'
            room.save()
            
            if user_type == 'user':
                return redirect('/my_bookings/')
            else:
                return redirect('/guest_bookings/')
                
        except (Room.DoesNotExist, Login.DoesNotExist, ValueError):
            return HttpResponse("Error processing booking")
            
    return redirect('/')

def user_bookings(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')
    resident = Resident.objects.get(id=request.session['resident_id'])
    bookings = Booking.objects.filter(user=resident.login)
    return render(request, 'USER/my_bookings.html', {'bookings': bookings})


def add_feedback_user(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')

    resident = Resident.objects.get(id=request.session['resident_id'])
    user = resident.login

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if not message:
            return render(request, 'USER/add_feedback.html', {
                'error': 'Feedback cannot be empty'
            })

        Feedback.objects.create(
            user=user,
            message=message,
            role_type='USER'
        )

        return redirect('/user_home/')

    return render(request, 'USER/add_feedback.html')


def view_feedback_user(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')
    
    resident = Resident.objects.get(id=request.session['resident_id'])
    feedbacks = Feedback.objects.filter(user=resident.login).order_by('-date')
    return render(request, 'USER/view_feedback.html', {'feedbacks': feedbacks})

def delete_feedback(request, id):
    login_id = None
    if 'resident_id' in request.session:
        login_id = request.session['resident_id']
        resident = Resident.objects.get(id=login_id)
        user = resident.login
    elif 'guest_id' in request.session:
        login_id = request.session['guest_id']
        guest = Guest.objects.get(id=login_id)
        user = guest.login
    elif request.user.is_authenticated and request.user.user_type == 'admin':
        # Admin can delete any feedback
        Feedback.objects.get(id=id).delete()
        return redirect('/view_feedback_admin/')
    else:
        return redirect('/login/')
        
    # For User/Guest, ensure they own the feedback
    try:
        feedback = Feedback.objects.get(id=id)
        if feedback.user == user:
            feedback.delete()
    except Feedback.DoesNotExist:
        pass
        
    if 'resident_id' in request.session:
        return redirect('/view_feedback_user/')
    else:
        return redirect('/view_guest_feedback/')



def add_feedback_guest(request):
    if 'guest_id' not in request.session:
        return redirect('/login/')

    guest = Guest.objects.get(id=request.session['guest_id'])
    user = guest.login

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if not message:
            return render(request, 'GUEST/add_feedback.html', {
                'error': 'Feedback cannot be empty'
            })

        Feedback.objects.create(
            user=user,
            message=message,
            role_type='GUEST'
        )

        return redirect('/guest_home/')

    return render(request, 'GUEST/add_feedback.html')





# New User Functions
def leave_request(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')
    
    resident = Resident.objects.get(id=request.session['resident_id'])
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        LeaveRequest.objects.create(resident=resident, reason=reason, start_date=start_date, end_date=end_date)
        return redirect('/my_leave_requests/')
    
    return render(request, 'USER/leave_request.html')

def my_leave_requests(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')
    
    resident = Resident.objects.get(id=request.session['resident_id'])
    leaves = LeaveRequest.objects.filter(resident=resident).order_by('-created_at')
    return render(request, 'USER/my_leave_requests.html', {'leaves': leaves})

def view_events_user(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')
    
    events = Event.objects.all().order_by('-date')
    return render(request, 'USER/view_events.html', {'events': events})

def view_fees_user(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')
    
    resident = Resident.objects.get(id=request.session['resident_id'])
    fees = Fee.objects.filter(user=resident.login).order_by('-created_at')
    return render(request, 'USER/view_fees.html', {'fees': fees})

# Guest Functions
def guest_bookings(request):
    if 'guest_id' not in request.session:
        return redirect('/login/')
    guest = Guest.objects.get(id=request.session['guest_id'])
    bookings = Booking.objects.filter(user=guest.login)
    return render(request, 'GUEST/my_bookings.html', {'bookings': bookings})

# def guest_feedback(request):
#     guest_id = request.session.get('guest_id')

#     if not guest_id:
#         return redirect('/login/')

#     try:
#         user = Login.objects.get(id=guest_id)
#     except Login.DoesNotExist:
#         return redirect('/login/')

#     if request.method == 'POST':
#         message = request.POST.get('message', '').strip()

#         if not message:
#             return render(request, 'GUEST/add_feedback.html', {
#                 'error': 'Feedback cannot be empty'
#             })

#         # SAVE FEEDBACK
#         Feedback.objects.create(
#             user=user,
#             name=user.guest.name,   # ✅ correct guest name
#             message=message,
#             role_type='GUEST'
#         )

#         return redirect('/guest_home/')

#     return render(request, 'GUEST/add_feedback.html')

def view_guest_feedback(request):
    if 'guest_id' not in request.session:
        return redirect('/login/')
    
    guest = Guest.objects.get(id=request.session['guest_id'])
    feedbacks = Feedback.objects.filter(user=guest.login).order_by('-date')
    return render(request, 'GUEST/view_feedback.html', {'feedbacks': feedbacks})

# Removed old make_payment to avoid duplication with confirm_payment
# def make_payment(request): ... 

# Attendance Views
def mark_attendance(request):
    if 'resident_id' not in request.session:
        return redirect('/login/')
    
    resident = Resident.objects.get(id=request.session['resident_id'])
    today = datetime.date.today()
    
    msg = ""
    if request.method == 'POST':
        if not Attendance.objects.filter(resident=resident, date=today).exists():
            Attendance.objects.create(resident=resident, date=today, status='PRESENT')
            msg = "Attendance marked successfully!"
        else:
            msg = "Attendance already marked for today."
            
    is_marked = Attendance.objects.filter(resident=resident, date=today).exists()
    
    # Show last 7 days history
    history = Attendance.objects.filter(resident=resident).order_by('-date')[:7]
    
    return render(request, 'USER/mark_attendance.html', {
        'is_marked': is_marked,
        'history': history,
        'today': today,
        'msg': msg
    })

def view_attendance_admin(request):
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        return redirect('/login/')
        
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
             selected_date = datetime.date.today()
    else:
        selected_date = datetime.date.today()
        
    residents = Resident.objects.all()
    attendance_data = []
    
    for res in residents:
        status = "ABSENT"
        att = Attendance.objects.filter(resident=res, date=selected_date).first()
        if att:
            status = "PRESENT"
            
        attendance_data.append({
            'name': res.name,
            'roll': res.roll_number,
            'status': status
        })
        
    return render(request, 'ADMIN/view_attendance.html', {
        'attendance_data': attendance_data,
        'selected_date': selected_date
    })
