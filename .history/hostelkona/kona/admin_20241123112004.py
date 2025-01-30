from django.contrib import admin
from django import forms
from .models import ManagerProfile, Hostel, Room
from django.contrib.auth.models import User

# Room Inline for displaying rooms inside the Hostel Admin
class RoomInline(admin.TabularInline):
    model = Room
    extra = 1  # Add an empty form to add a room
    fields = ['room_number', 'room_type', 'is_available', 'price']
    readonly_fields = ['room_number']

    def get_queryset(self, request):
        """
        This method limits the rooms to the current hostel in the inline.
        It ensures that only rooms related to the current hostel are shown.
        """
        queryset = super().get_queryset(request)
        
        # Use self.instance to get the parent Hostel object
        if self.instance:
            # Filter rooms based on the parent hostel instance
            return queryset.filter(hostel=self.instance)
        return queryset

# Manager Profile Admin
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


# Hostel Admin
@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'number_of_rooms', 'is_active'] 
    search_fields = ['name']
    list_filter = ['is_active', 'manager']  

    # To handle the inline Room management
    inlines = [RoomInline]  # Display rooms inline in the hostel admin page

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Limit queryset to hostels managed by the logged-in user
        return queryset.filter(manager=request.user)


# Room Admin
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hostel', 'room_type', 'is_available']
    list_filter = ['hostel', 'room_type', 'is_available']
    search_fields = ['room_number']

    # Limit queryset to rooms within the logged-in user's hostels
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(hostel__manager=request.user)
