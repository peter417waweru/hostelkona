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
        Return rooms linked to the current hostel being edited.
        """
        queryset = super().get_queryset(request)
        if hasattr(self, 'parent_object') and self.parent_object:
            return queryset.filter(hostel=self.parent_object)
        return queryset

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Ensure the 'hostel' field is set to the parent hostel for inline forms.
        """
        if db_field.name == 'hostel' and hasattr(self, 'parent_object'):
            kwargs['queryset'] = Hostel.objects.filter(id=self.parent_object.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

    # Inline for managing rooms within a hostel
    inlines = [RoomInline]

    def get_form(self, request, obj=None, **kwargs):
        """
        Make the parent hostel instance accessible to the inline form.
        """
        if obj:
            # Pass the parent hostel instance to the inline
            self.inlines[0].parent_object = obj
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        """
        Limit hostels to those managed by the logged-in user.
        """
        queryset = super().get_queryset(request)
        return queryset.filter(manager=request.user)


# Room Admin
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hostel', 'room_type', 'is_available']
    list_filter = ['hostel', 'room_type', 'is_available']
    search_fields = ['room_number']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(hostel__manager=request.user)
