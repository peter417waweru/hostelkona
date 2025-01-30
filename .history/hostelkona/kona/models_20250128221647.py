from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User 
from django.utils import timezone




class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=40, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Hostel(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('suite', 'Suite'),
        ('bedsitter', 'Bedsitter'),
        ('one-bedroom', 'One Bedroom'),
    ]

    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hostels')
    Images = models.ImageField(upload_to='hostel_images/')
    description = models.TextField()
    amenities = models.TextField()
    address = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_rooms = models.PositiveIntegerField(default=0)  # The number of rooms in the hostel
    default_room_image = models.ImageField(
        upload_to='room_images/', 
        blank=True, 
        null=True,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('suite', 'Suite'),
        ('bedsitter', 'Bedsitter'),
        ('one-bedroom', 'One Bedroom'),
    ]

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    images = models.ImageField(upload_to='room_images/', blank=True, null=True)
    room_number = models.CharField(max_length=10, unique=True)  # Room number should be unique
    is_available = models.BooleanField(default=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, blank=True, null=True)  # Use choices for room types
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hostel', 'room_number'], name='unique_room_number_per_hostel')
        ]

    def __str__(self):   
        return f"Room {self.room_number} - {self.room_type}"



class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    search_date = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.hostel.name}"
    

class BookingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_requests")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True) 
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.name} - {self.status}"

   
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    receipt_id = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.receipt_id} - {self.user.username}"


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='default_profile_picture.jpg')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
