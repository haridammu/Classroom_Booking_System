from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('book-room/', views.book_room, name='book_room'),
    path('view-schedule/', views.view_schedule, name='view_schedule'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),  # Teacher Dashboard
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),  # Add this for student dashboard
    path('view-all-bookings/', views.view_all_bookings, name='view_all_bookings'),
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
]

