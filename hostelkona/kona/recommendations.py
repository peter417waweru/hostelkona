from django.db.models import Count
from django.conf import settings  # For referencing AUTH_USER_MODEL
from .models import Hostel, UserSearchHistory


def get_related_hostels(user):
    # Get recent searches for the current user
    recent_searches = UserSearchHistory.objects.filter(user=user).values('hostel__address', 'hostel__amenities')

    # Find the most common address from the user's search history
    common_address = recent_searches.values('hostel__address').annotate(count=Count('hostel__address')).order_by('-count').first()
    common_address_value = common_address['hostel__address'] if common_address else None

    # Find the most common amenities from the user's search history
    common_amenities = recent_searches.values('hostel__amenities').annotate(count=Count('hostel__amenities')).order_by('-count').first()
    common_amenities_value = common_amenities['hostel__amenities'] if common_amenities else None

    # Build filter criteria based on common address and amenities
    filter_criteria = {}
    if common_address_value:
        filter_criteria['address'] = common_address_value
    if common_amenities_value:
        filter_criteria['amenities__icontains'] = common_amenities_value

    # Fetch related hostels, excluding those already searched by the user
    related_hostels = Hostel.objects.filter(**filter_criteria).exclude(
        id__in=UserSearchHistory.objects.filter(user=user).values_list('hostel__id', flat=True)
    )[:10]

    return related_hostels
