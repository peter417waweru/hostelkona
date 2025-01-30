from django.contrib import admin
from django import forms
from .models import ManagerProfile
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
