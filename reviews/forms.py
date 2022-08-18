from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    template_name = 'reviews/leave_review_form.html'

    class Meta:
        model = Review
        fields = ['score', 'comment']
