from django import forms
from .models import Room, Booking, Hostel, BookingRequest, ManagerProfile
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
        fields = ['name', 'Images', 'description', 'amenities', 'address', 'contact_no', 'email', 'default_room_image']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price', 'images', 'is_available']
        widgets = {
            'room_type': forms.Select(choices=Room.ROOM_TYPE_CHOICES),  # Add a dropdown for room types
        }
        
class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['message']  

class ManagerProfileForm(forms.ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ['profile_picture', 'contact_number']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
