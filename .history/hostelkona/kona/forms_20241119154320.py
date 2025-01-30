from django import forms
from .models import Room, Booking, Hostel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HostelCustomerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hostel', 'room','start_date']


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'Images', 'description', 'amenities', 'address', 'contact_no', 'email']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price', 'images', 'is_available']
        widgets = {
            'room_type': forms.Select(),
        }