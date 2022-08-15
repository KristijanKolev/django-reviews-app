from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('places', views.AllPlacesView.as_view(), name='all_places'),
    path('places/<int:pk>', views.PlaceDetailsPublic.as_view(), name='place_details_public'),
]
