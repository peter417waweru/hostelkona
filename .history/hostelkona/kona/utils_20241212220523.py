from django.contrib.auth.models import Group

def is_hostel_manager(user):
    return user.groups.filter(name='Hostel Manager').exists()
