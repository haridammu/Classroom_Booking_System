from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import time

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.DateTimeField()  # Updated to DateTimeField

    booked_by = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return f"Booking for {self.room} on {self.date} at {self.time_slot} by {self.user.username}"

    def send_booking_email(self):
        subject = 'Room Booking Confirmation'
        message = f"Your room booking for {self.room.name} on {self.date} at {self.time_slot} is confirmed."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.user.email]
        send_mail(subject, message, email_from, recipient_list)
