from django.core.cache import cache
from service.models.location_model import Location
from service.models.search_log_model import SearchLog

class LocationService:
    @classmethod
    def get_or_fetch_location(cls, query):
        query = query.strip().lower()
        cache_key = f"loc_{query.replace(' ', '_')}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return {"data": cached_data, "status": "SUCCESS"}

        location = Location.objects.filter(name__icontains=query).first()
        if location:
            cache.set(cache_key, location, 3600)
            return {"data": location, "status": "SUCCESS"}

        SearchLog.objects.update_or_create(
            query=query,
            defaults={'status': 'PENDING', 'is_processed': False}
        )

        return {
            "message": "Location request received. Our background worker is fetching details. Please refresh in 2-3 seconds.",
            "status": "PROCESSING"
        }