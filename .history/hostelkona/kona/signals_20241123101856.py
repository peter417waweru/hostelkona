from django.db.models.signals import post_save,  post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ManagerProfile, Room, Hostel

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        ManagerProfile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(post_save, sender=Room)
def update_room_count_on_save(sender, instance, **kwargs):
    """
    Updates the number_of_rooms field in the associated hostel when a room is added or updated.
    """
    hostel = instance.hostel
    hostel.number_of_rooms = Room.objects.filter(hostel=hostel).count()
    hostel.save()

@receiver(post_delete, sender=Room)
def update_room_count_on_delete(sender, instance, **kwargs):
    """
    Updates the number_of_rooms field in the associated hostel when a room is deleted.
    """
    hostel = instance.hostel
    hostel.number_of_rooms = Room.objects.filter(hostel=hostel).count()
    hostel.save()