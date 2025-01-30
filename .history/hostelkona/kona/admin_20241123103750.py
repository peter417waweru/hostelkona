from django.contrib import admin
from django import forms
from .models import ManagerProfile, Hostel, Room
from django.contrib.auth.models import User

class ManagerProfileForm(forms.ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ['profile_picture', 'contact_number']

class ManagerProfileAdmin(admin.ModelAdmin):
    form = ManagerProfileForm
    list_display = ['user', 'profile_picture', 'contact_number']

    def save_model(self, request, obj, form, change):
        # Ensure that if no profile image is uploaded, the default is used
        if not obj.profile_picture:
            obj.profile_picture = 'default_profile_picture.jpg'
        super().save_model(request, obj, form, change)

admin.site.register(ManagerProfile, ManagerProfileAdmin)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'number_of_rooms', 'is_active'] 
    search_fields = ['name']
    list_filter = ['is_active', 'manager']  


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hostel', 'room_type', 'is_available']
    list_filter = ['hostel', 'room_type', 'is_available']
    search_fields = ['room_number']




