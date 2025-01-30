from django import forms
from .models import Room, Booking, Hostel, BookingRequest, ManagerProfile, RoomType
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
    room_types = forms.ModelMultipleChoiceField(
        queryset=RoomType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Hostel
        fields = ['name', 'manager', 'Images', 'description', 'amenities', 'address', 
                  'contact_no', 'email', 'number_of_rooms', 'room_types', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'Images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'number_of_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price', 'is_available', 'images']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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
