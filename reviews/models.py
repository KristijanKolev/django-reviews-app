from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def average_review_score(self):
        return sum(review.score for review in
                   self.review_set.all()) / self.review_set.count() if self.review_set.count() > 0 else None

    def sorted_reviews(self):
        return self.review_set.all().order_by('-id')


class Review(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.CharField(max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.place.name}: {self.score}'
