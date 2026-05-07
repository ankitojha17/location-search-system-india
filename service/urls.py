from django.urls import path
from service.views.location_search_view import LocationSearchView

urlpatterns = [
    path('location/search', LocationSearchView.as_view(), name='location_search'),
]