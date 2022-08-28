from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView

from .models import Place, Review
from .forms import ReviewForm, PlaceForm
from .decorators import user_can_edit_place


class AllPlacesView(generic.ListView):
    model = Place
    template_name = 'reviews/all_places.html'
    default_page_size = 5

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.default_page_size)

    def get_queryset(self):
        search_term = self.request.GET.get('search')
        query_set = super().get_queryset()
        if search_term:
            query_set = query_set.filter(name__icontains=search_term)
        return query_set.order_by('-date_created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search')
        if search_term:
            context['search'] = search_term
        return context


class PlaceDetailsPublic(LoginRequiredMixin, generic.DetailView):
    model = Place
    template_name = 'reviews/place_details_public.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context


@login_required
def place_create_view(request):
    context = {}
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        context['form'] = form
        if form.is_valid():
            place = form.save(commit=False)
            place.owner = request.user
            place.save()

            return HttpResponseRedirect(reverse('reviews:places_all'))
    else:
        context['form'] = PlaceForm()

    return render(request, 'reviews/create_place.html', context)


@login_required
@user_can_edit_place
def place_edit_view(request, pk):
    place = get_object_or_404(Place, pk=pk)
    context = {'place': place}
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        context['form'] = form
        if form.is_valid():
            place.name = form.cleaned_data['name']
            place.description = form.cleaned_data['description']
            place.save()

            return HttpResponseRedirect(reverse('reviews:places_all'))
    else:
        context['form'] = PlaceForm(instance=place)

    return render(request, 'reviews/edit_place.html', context)


@login_required
def leave_review(request, pk):
    place = get_object_or_404(Place, pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        place.review_set.create(score=form.cleaned_data['score'], comment=form.cleaned_data['comment'],
                                author=request.user)
        return HttpResponseRedirect(reverse('reviews:place_details_public', args=(place.id,)))
    else:
        context = {
            'place': place,
            'review_form': form
        }

        return render(request, 'reviews/place_details_public.html', context)


