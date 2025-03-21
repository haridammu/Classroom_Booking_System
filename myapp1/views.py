from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import Room, Booking
from django.core.mail import send_mail
from django.conf import settings

# Home Page View
def home(request):
    # Prevent students from accessing the home page
    if request.user.groups.filter(name='Student').exists():
        return redirect('student_dashboard')  # Redirect students directly to their dashboard
    return render(request, 'home.html')

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_based_on_role(request)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Redirect Based on Role
def redirect_based_on_role(request):
    user = request.user
    if user.is_staff:
        messages.success(request, f'Welcome back, {user.username} (Admin)!')
        return redirect('admin_dashboard')
    elif user.groups.filter(name='Teacher').exists():
        messages.success(request, f'Welcome back, {user.username} (Teacher)!')
        return redirect('teacher_dashboard')
    elif user.groups.filter(name='Student').exists():
        messages.success(request, f'Welcome back, {user.username} (Student)!')
        return redirect('student_dashboard')
    else:
        messages.error(request, 'User has no assigned role.')
        return redirect('home')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

# Room Booking View
def book_room(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        date = request.POST.get('date')
        user = request.user
        room = Room.objects.get(id=room_id)

        if Booking.objects.filter(room=room, date=date).exists():
            messages.error(request, 'This room is already booked on the selected date. Please choose a different date.')
            return redirect('book_room')

        booking = Booking(room=room, date=date, user=user, booked_by=user.username)
        booking.save()

        send_booking_email(booking)
        messages.success(request, f'Your booking for {room.name} on {date} is confirmed.')
        return redirect('view_schedule')

    booked_rooms = Booking.objects.filter(date=timezone.now().date()).values('room_id')
    available_rooms = rooms.exclude(id__in=booked_rooms)

    return render(request, 'book_room.html', {'rooms': available_rooms})

# View Schedule
def view_schedule(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'view_schedule.html', {'bookings': bookings})

# Send Booking Confirmation Email
def send_booking_email(booking):
    subject = 'Room Booking Confirmation'
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.room.name} on {booking.date} is confirmed."
    from_email = settings.EMAIL_HOST_USER
    to_email = [booking.user.email]
    send_mail(subject, message, from_email, to_email)

# Signup View
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')

        if form.is_valid():
            user = form.save()

            if role:
                try:
                    group = Group.objects.get(name=role)
                    user.groups.add(group)
                except Group.DoesNotExist:
                    messages.error(request, "The selected role doesn't exist.")
                    return redirect('signup')
            else:
                messages.error(request, "Please select a role.")
                return redirect('signup')

            login(request, user)

            if role == 'Admin':
                messages.success(request, 'Account created successfully! You are now logged in as Admin.')
                return redirect('admin_dashboard')
            elif role == 'Teacher':
                messages.success(request, 'Account created successfully! You are now logged in as Teacher.')
                return redirect('teacher_dashboard')
            elif role == 'Student':
                messages.success(request, 'Account created successfully! You are now logged in as Student.')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Unknown role selected.')
                return redirect('home')

        else:
            messages.error(request, f'There was an error creating your account: {form.errors}')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

# Admin Dashboard View
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Teacher Dashboard View
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

# Student Dashboard View
from django.contrib.auth.models import Group

from django.shortcuts import render
from .models import Booking, Room  # Import Booking and Room models
from django.contrib.auth.models import Group

# Student Dashboard View
def student_dashboard(request):
    if not request.user.groups.filter(name='Student').exists():
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    # Fetch the student's own bookings
    student_bookings = Booking.objects.filter(user=request.user)

    # Fetch all bookings made by teachers
    teacher_group = Group.objects.get(name='Teacher')
    teacher_bookings = Booking.objects.filter(user__groups=teacher_group)

    # Fetch all available rooms
    available_rooms = Room.objects.all()

    return render(request, 'student_dashboard.html', {
        'student_bookings': student_bookings,
        'teacher_bookings': teacher_bookings,
        'available_rooms': available_rooms,  # Pass the available rooms to the template
    })


from django.shortcuts import render
from .models import Booking  # Ensure that you import the necessary model

# View to show all bookings (for admin)
def view_all_bookings(request):
    bookings = Booking.objects.all()  # Fetch all bookings from the database
    return render(request, 'view_all_bookings.html', {'bookings': bookings})
# myapp1/views.py

from django.shortcuts import render
from .models import Room  # Make sure to import your Room model

# View for managing rooms (for admin)
def manage_rooms(request):
    rooms = Room.objects.all()  # Fetch all rooms from the database
    return render(request, 'manage_rooms.html', {'rooms': rooms})
from django.core.mail import send_mail
from django.conf import settings
import logging

def send_booking_email(booking):
    subject = 'Room Booking Confirmation'
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.room.name} on {booking.date} is confirmed."
    from_email = settings.EMAIL_HOST_USER
    to_email = [booking.user.email]

    try:
        send_mail(subject, message, from_email, to_email)
        logging.info(f"Booking confirmation email sent to {booking.user.email}")
    except Exception as e:
        logging.error(f"Failed to send booking confirmation email: {e}")
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room
from .forms import RoomForm  # Assuming you have a form for Room

def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('manage_rooms')  # Redirect to the rooms management page
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'edit_room.html', {'form': form})
# views.py
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect('manage_rooms')  # Redirect to the rooms management page
