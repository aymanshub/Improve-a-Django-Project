from django.db import models
from django.utils import timezone
from _datetime import date


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateField(default=date.today)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')
    created_date = models.DateField(default=date.today)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
