"""
URL configuration for hostel project.
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('user_register/', views.register_resident),
    path('guest_register/', views.register_guest),
    path('login/', views.login_view),
    path('logout/', views.auth_logout, name='logout'),

    # Home Pages
    path('', views.index),
    path('user_home/', views.user_index),
    path('guest_home/', views.guest_index),
    path('admin_home/', views.admin_index),

    # Admin Features
    path('view_rooms/', views.view_rooms),
    path('add_room/', views.add_room),
    path('update_room_status/', views.update_room_status),
    path('edit_room/<int:id>/', views.edit_room),
    path('delete_room/<int:id>/', views.delete_room),
    path('manage_mess/', views.manage_mess),
    path('view_bookings_admin/', views.view_bookings_admin),
    path('approve_booking/', views.approve_booking),
    path('reject_booking/', views.reject_booking),
    path('view_feedback_admin/', views.view_feedback_admin),
    path('view_users/', views.view_users),
    path('block_user/', views.block_user),
    path('unblock_user/', views.unblock_user),
    path('view_guest/', views.view_guests),
    path('manage_events/', views.manage_events),
    path('delete_event/', views.delete_event),
    path('view_leave_requests/', views.view_leave_requests),
    path('approve_leave/', views.approve_leave),
    path('reject_leave/', views.reject_leave),
    path('manage_fees/', views.manage_fees),
    path('add_fee/', views.add_fee),
    path('mark_fee_paid/', views.mark_fee_paid),
    path('view_attendance_admin/', views.view_attendance_admin),

    # User Features
    path('view_mess_user/', views.view_mess_user),
    path('book_room/', views.book_room),
    path('place_booking/', views.place_booking),
    path('my_bookings/', views.user_bookings),
    path('user_add_feedback/', views.add_feedback_user),
    path('view_feedback_user/', views.view_feedback_user),
    path('delete_feedback/<int:id>/', views.delete_feedback),
    path('leave_request/', views.leave_request),
    path('my_leave_requests/', views.my_leave_requests),
    path('view_events_user/', views.view_events_user),
    path('view_fees_user/', views.view_fees_user),
    # path('view_guest_feedback/', views.view_guest_feedback),
    path('mark_attendance/', views.mark_attendance),

    # Guest Features
    path('guest_bookings/', views.guest_bookings),
    path('guest_add_feedback/', views.add_feedback_guest),
    path('confirm_payment/', views.confirm_payment),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
