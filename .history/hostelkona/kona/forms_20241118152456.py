from django import forms
from .models import Room, Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HostelCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hostel', 'room','start_date']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'room_number', 'is_available', 'price']