from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('register/', views.customer_register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('hostels/<int:hostel_id>/rooms/', views.hostel_rooms, name='hostel_rooms'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('application-success/', views.application_success, name='application_success'),
    
    path('about-us/', views.about_us, name='about_us'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('cart/', views.view_cart, name='cart'),
    path('help/', views.help_page, name='help'),

    path('download-receipt/<str:receipt_id>/', views.download_receipt, name='download_receipt'),
    path('dashboard/download-pdf/', views.download_dashboard_pdf, name='download_dashboard_pdf'),
    path('dashboard/', views.dashboard, name='dashboard'),

    
    path('<int:hostel_id>/detail/', views.hostel_details, name='hostel_details'),
    path('dashboard/my-hostels/', views.manager_hostels, name='manager_hostels'),
    path('booking_success/', views.booking_success, name='booking_success'),

    path('dashboard/add-hostel/', views.add_hostel, name='add_hostel'),
    path('dashboard/update-hostel/<int:pk>/', views.update_hostel, name='update_hostel'),
    path('dashboard/delete-hostel/<int:hostel_id>/', views.delete_hostel, name='delete_hostel'),
    path('hostel/<int:hostel_id>/add-room/', views.add_room, name='add_room'),

    path('room/<int:id>/update/', views.update_room, name='update_room'),
    path('room/<int:id>/delete/', views.delete_room, name='delete_room'),
    path('update-profile/', views.update_profile, name='update_profile'),

    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('dashboard/view_booking_requests/', views.view_booking_requests, name='view_booking_requests'),
    path('requests/<int:request_id>/', views.manage_booking_request, name='manage_booking_request'),

    path('settings/', views.settings_view, name='settings'),
    path('update_settings/', views.update_settings, name='update_settings'),
    
    path('analytics/', views.analytics_view, name='analytics'),
    path('api/occupancy-rate/', views.occupancy_rate, name='occupancy_rate'),
    path('messages/', views.messages_page, name='messages_page'),
    path('messages/send/', views.send_message, name='send_message'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)