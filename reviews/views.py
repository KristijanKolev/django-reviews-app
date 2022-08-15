from django.shortcuts import render
from django.views import generic

from .models import Place, Review


class AllPlacesView(generic.ListView):
    model = Place
    template_name = 'reviews/all_places.html'


class PlaceDetailsPublic(generic.DetailView):
    model = Place
    template_name = 'reviews/place_details_public.html'

