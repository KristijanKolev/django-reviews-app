from django import forms

from .models import Review, Place


class ReviewForm(forms.ModelForm):
    template_name = 'reviews/forms/leave_review_form.html'

    class Meta:
        model = Review
        fields = ['score', 'comment']


class PlaceForm(forms.ModelForm):
    template_name = 'reviews/forms/place_form.html'

    class Meta:
        model = Place
        fields = ['name', 'description']
