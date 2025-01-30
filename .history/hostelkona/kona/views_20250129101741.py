from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Hostel, Room, BookingRequest, Notification, Customer, Booking, Transaction, ManagerProfile, UserSearchHistory, User, Message
from .forms import HostelForm, RoomForm, BookingRequestForm, ManagerProfileForm
from django.contrib.auth import get_user_model
from .forms import HostelCustomerForm
from django.contrib import messages
from django.db.models import Q
from .recommendations import get_related_hostels
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Count, Sum

@login_required(login_url='login')
def hostel_details(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    related_hostels = get_related_hostels(request.user)
    rooms = hostel.rooms.filter(is_available=True)
    return render(request, 'customer/hostel_details.html', {'hostel': hostel, 'related_hostels': related_hostels,'rooms': rooms})

def customer_register(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        form = HostelCustomerForm()
        if request.method == 'POST':
            form = HostelCustomerForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard' if request.user.groups.filter(name='Hostel_Managers').exists() else 'home_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.groups.filter(name='Hostel_Managers').exists():
                return redirect('dashboard')  # Redirect to manager dashboard
            return redirect('home_page')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home_page')

@login_required(login_url='login')
def profile_view(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.username, 'email': request.user.email}
    )

    # Retrieve the accepted booking request
    accepted_booking = BookingRequest.objects.filter(user=request.user, status='Accepted').select_related('room', 'room__hostel').first()

    # Retrieve all transactions for the user
    transactions = Transaction.objects.filter(user=request.user)

    # Retrieve unread notifications
    notifications = request.user.notifications.filter(is_read=False)
    

    context = {
        'customer': customer,
        'created': created,
        'current_booking': accepted_booking.room if accepted_booking else None,
        'transactions': transactions,
        'notifications': notifications,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def application_success(request):
    return render(request, 'customer/application_success.html')


def home_page(request):
    q = request.GET.get('q', '')
    hostels = Hostel.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q),
        is_active=True  # Only show active hostels
    )

    hostel_counts = hostels.count()
    rooms = Room.objects.filter(hostel__is_active=True)[:10]  # Rooms of active hostels only

    context = {
        'rooms': rooms,
        'hostels': hostels,
        'hostel_count': hostel_counts
    }
    return render(request, 'customer/home_page.html', context)


def booking_success(request):
    return render(request, 'customer/application_success.html')


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if not room.is_available:
        messages.error(request, "This room is no longer available.")
        return redirect('home_page')

    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking_request = form.save(commit=False)
            booking_request.user = request.user
            booking_request.room = room
            booking_request.status = 'Pending'
            booking_request.save()

            messages.success(request, "Your booking request has been sent successfully!")
            return redirect('profile')

    form = BookingRequestForm()
    return render(request, 'customer/apply_room.html', {
        'room': room,
        'form': form,
    })



@login_required
def hostel_rooms(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    available_rooms = hostel.rooms.filter(is_available=True)
    context = {
        'hostel': hostel,
        'available_rooms': available_rooms,
    }
    return render(request, 'customer/hostel_rooms.html', context)


@login_required
def dashboard(request):
    """
    View for manager's dashboard, determining if the user is a hostel manager and 
    displaying stats like new requests, tenants, and revenue.
    """
    is_hostel_manager = request.user.groups.filter(name='Hostel_Managers').exists()

    if is_hostel_manager:
        # Fetch data specific to managers
        managed_hostels = Hostel.objects.filter(manager=request.user)
        booking_requests = BookingRequest.objects.filter(room__hostel__in=managed_hostels)
        new_requests_count = booking_requests.filter(status='Pending').count()
        tenant_count = Booking.objects.filter(approved=True, room__hostel__in=managed_hostels).count()

        # Sum the total rent from approved bookings
        total_rent = (
            Booking.objects.filter(approved=True, room__hostel__in=managed_hostels)
            .aggregate(total=Sum('room__price'))['total']
            or 0
        )

        # Fetch recent booking requests, sorted by submission date
        recent_requests = booking_requests.order_by('-date_submitted')[:7]

        context = {
            'is_hostel_manager': is_hostel_manager,
            'new_requests_count': new_requests_count,
            'tenant_count': tenant_count,
            'total_rent': total_rent,
            'recent_requests': recent_requests,
        }
    else:
        # Context for non-managers (customers)
        context = {
            'is_hostel_manager': is_hostel_manager,
        }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def update_profile(request):
    profile = request.user.profile  # Access the ManagerProfile
    if request.method == 'POST':
        form = ManagerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error updating your profile. Please check the details.")
    else:
        form = ManagerProfileForm(instance=profile)

    return render(request, 'dashboard/update_profile.html', {'form': form})

@login_required
def download_dashboard_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dashboard.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Dashboard Overview")
    p.drawString(100, 780, f"New Requests: {BookingRequest.objects.filter(status='Pending').count()}")
    p.drawString(100, 760, f"Tenants: {Booking.objects.filter(approved=True).count()}")
    p.drawString(100, 740, f"Total Rent: ${Booking.objects.filter(approved=True).aggregate(total=Sum('room__price'))['total'] or 0}")
    p.showPage()
    p.save()

    return response


@login_required
def manager_hostels(request):
    hostels = Hostel.objects.filter(manager=request.user)
    return render(request, 'dashboard/my_hostels.html', {'hostels': hostels})


@login_required
def add_hostel(request):
    hostel_form = HostelForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if hostel_form.is_valid():
            hostel = hostel_form.save(commit=False)
            hostel.manager = request.user
            hostel.save()

            messages.success(
                request,
                f"The hostel '{hostel.name}' has been successfully created! "
                "You can now add rooms to this hostel."
            )
            return redirect('manager_hostels')  
        else:
            messages.error(request, "There was an error creating the hostel. Please try again.")

    return render(request, 'dashboard/add_hostel.html', {
        'hostel_form': hostel_form,
    })

@login_required
def add_room(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id, manager=request.user)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hostel = hostel
            room.save()

            messages.success(
                request,
                f"Room '{room.room_number}' added successfully to '{hostel.name}'!"
            )
            return redirect('add_room', hostel_id=hostel.id) 
        else:
            messages.error(request, "There was an error adding the room. Please try again.")
    else:
        form = RoomForm()

    return render(request, 'dashboard/add_room.html', {
        'hostel': hostel,
        'form': form,
    })

@login_required
def update_hostel(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk, manager=request.user)
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES, instance=hostel)
        if form.is_valid():
            form.save()
            return redirect('manager_hostels')
    else:
        form = HostelForm(instance=hostel)
    return render(request, 'dashboard/update_hostel.html', {'form': form})

@login_required
def delete_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id, manager=request.user)
    
    if request.method == 'POST':
        # Delete the hostel
        hostel.delete()
        messages.success(request, f"The hostel '{hostel.name}' has been successfully deleted.")
        return redirect('manager_hostels')  

    return render(request, 'dashboard/delete_hostel.html', {'hostel': hostel})

@login_required
def manage_rooms(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id, manager=request.user)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hostel = hostel  
            room.save()
            return redirect('manage_rooms', hostel_id=hostel.id)
    else:
        form = RoomForm()
    rooms = hostel.rooms.all()
    return render(request, 'dashboard/manage_rooms.html', {'hostel': hostel, 'rooms': rooms, 'form': form})

@login_required
def view_booking_requests(request):
    booking_requests = BookingRequest.objects.filter(room__hostel__manager=request.user)

    return render(request, 'dashboard/view_booking_requests.html', {
        'booking_requests': booking_requests
    })

@login_required
def manage_booking_request(request, request_id):
    booking_request = get_object_or_404(
        BookingRequest,
        id=request_id,
        room__hostel__manager=request.user
    )

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            if booking_request.room.bookingrequest_set.filter(status='Accepted').exists():
                messages.error(request, "This room has already been booked.")
                return redirect('dashboard')

            booking_request.status = 'Accepted'
            booking_request.save()

            # Update room status
            booking_request.room.is_available = False
            booking_request.room.save()

            # Create Booking
            Booking.objects.create(
                user=booking_request.user,
                room=booking_request.room,
                start_date=booking_request.start_date,
                approved=True
            )

            # Send Notification
            Notification.objects.create(
                user=booking_request.user,
                message=f"Your booking request for Room {booking_request.room.room_number} has been accepted."
            )
            messages.success(request, "Request has been accepted.")
        elif action == 'reject':
            booking_request.status = 'Rejected'
            booking_request.save()

            Notification.objects.create(
                user=booking_request.user,
                message=f"Your booking request for Room {booking_request.room.room_number} has been rejected."
            )
            messages.success(request, "Request has been rejected.")

        return redirect('dashboard')

    return render(request, 'dashboard/request_detail.html', {
        'booking_request': booking_request
    })


@login_required
def update_room(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully!")
            return redirect('manager_hostels')  # Redirect back to the hostels page
    else:
        form = RoomForm(instance=room)

    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'dashboard/update_room.html', context)


@login_required
def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted successfully!")
        return redirect('manager_hostels')
    return render(request, 'dashboard/confirm_delete.html', {'room': room})

@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        request.user.notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read.")
    return redirect('profile')


def download_receipt(request, receipt_id):
    transaction = get_object_or_404(Transaction, receipt_id=receipt_id, user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{receipt_id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Receipt ID: {transaction.receipt_id}")
    p.drawString(100, 780, f"Date: {transaction.date}")
    p.drawString(100, 760, f"Amount: ${transaction.amount}")
    p.drawString(100, 740, f"Hostel: {transaction.booking.hostel.name}")
    p.drawString(100, 720, f"Room: {transaction.booking.room.room_number}")
    p.showPage()
    p.save()

    return response


def about_us(request):
    return render(request, 'pages/about_us.html')

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'pages/terms_conditions.html')

def contact_us(request):
    return render(request, 'pages/contact_us.html')

def view_cart(request):
    return render(request, 'accounts/cart.html')

def help_page(request):
    return render(request, 'pages/help.html')

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')

@login_required
def update_settings(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST.get('password', None)
        language = request.POST['language']

        # Update email and username
        user = request.user
        user.email = email
        user.username = username

        if password:
            user.set_password(password)
        
        user.save()

        # Add language preference to user profile if applicable
        # Assuming you have a field for language preference in the user model

        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    else:
        return redirect('settings')


def analytics_view(request):
    # Total bookings
    total_bookings = Booking.objects.count()

    # Approved vs. pending bookings
    approved_bookings = Booking.objects.filter(approved=True).count()
    pending_bookings = Booking.objects.filter(approved=False).count()

    # Bookings per hostel
    bookings_per_hostel = list(Booking.objects.values('hostel__name').annotate(total=Count('id')))

    # Available vs. occupied rooms
    available_rooms = Room.objects.filter(is_available=True).count()
    occupied_rooms = Room.objects.filter(is_available=False).count()

    # Revenue generated
    total_revenue = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0
    revenue_per_hostel = list(Transaction.objects.values('booking__hostel__name').annotate(total=Sum('amount')))

    # Booking requests by status
    requests_by_status = list(BookingRequest.objects.values('status').annotate(total=Count('id')))

    # Most searched hostels
    most_searched_hostels = list(
        UserSearchHistory.objects.values('hostel__name').annotate(search_count=Count('id')).order_by('-search_count')[:5]
    )

    # Context for the template
    context = {
        'total_bookings': total_bookings,
        'approved_bookings': approved_bookings,
        'pending_bookings': pending_bookings,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'total_revenue': total_revenue,
        'bookings_per_hostel': bookings_per_hostel,
        'revenue_per_hostel': revenue_per_hostel,
        'requests_by_status': requests_by_status,
        'most_searched_hostels': most_searched_hostels,
    }
    return render(request, 'dashboard/analytics.html', context)


def occupancy_rate(request):
    # Get date range from the request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    # If no dates are provided, default to this month's range
    if not start_date or not end_date:
        start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch total rooms
    total_rooms = Room.objects.count()
    
    # Fetch occupied rooms within the given date range
    occupied_rooms = Booking.objects.filter(
        start_date__lte=end_date,
        end_date__gte=start_date
    ).count()
    
    # Calculate occupancy rate
    occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
    
    # Return the response as JSON
    return JsonResponse({
        'start_date': start_date,
        'end_date': end_date,
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'occupancy_rate': round(occupancy_rate, 2)
    })


@login_required
def messages_page(request):
    """Display inbox messages for the logged-in user."""
    inbox_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')

    # Decrypt messages before sending to the template
    for msg in inbox_messages:
        msg.decrypted_content = msg.decrypt_message()

    for msg in sent_messages:
        msg.decrypted_content = msg.decrypt_message()

    return render(request, 'messages.html', {
        'inbox_messages': inbox_messages,
        'sent_messages': sent_messages,
    })

@login_required
def send_message(request):
    """Send an encrypted message from the sender to the receiver."""
    if request.method == "POST":
        recipient_username = request.POST.get('recipient')
        content = request.POST.get('message')
        recipient = get_object_or_404(User, username=recipient_username)

        # Create and encrypt message
        message = Message(sender=request.user, receiver=recipient)
        message.encrypted_content = message.encrypt_message(content)
        message.save()

        return redirect('messages_page')

    return redirect('messages_page')

@login_required
def reply_message(request, message_id):
    """Allow a manager to reply to a message."""
    original_message = get_object_or_404(Message, id=message_id, receiver=request.user)

    if request.method == "POST":
        content = request.POST.get('reply')
        sender = request.user  # Manager replying
        receiver = original_message.sender  # Customer who asked the question

        reply_message = Message(sender=sender, receiver=receiver)
        reply_message.encrypted_content = reply_message.encrypt_message(content)
        reply_message.save()

        return redirect('messages_page')

    return render(request, 'reply_message.html', {'message': original_message})
