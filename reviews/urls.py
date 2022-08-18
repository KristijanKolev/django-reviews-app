from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.AllPlacesView.as_view(), name='places_all'),
    path('places/<int:pk>', views.PlaceDetailsPublic.as_view(), name='place_details_public'),
    path('places/<int:pk>/leave-review', views.leave_review, name='leave_review'),
]
