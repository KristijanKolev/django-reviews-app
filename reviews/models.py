from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date_created = models.DateField(auto_now_add=True)


class Review(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.CharField(max_length=500)
