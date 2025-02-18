from django.db import models
from django.contrib.auth.models import User

RSVP_STATUS = (
  ('I', 'Invited'),
  ('A', 'Attending'),
  ('N', 'Not attending'),
  ('M', 'Maybe')
)

DISH_CATEGORY = (
  ('A', 'Appetizer'),
  ('M', 'Main'),
  ('S', 'Side'),
  ('D', 'Dessert'),
  ('B', 'Beverage')
)

PARTY_STATUS = (
  ('A', 'Active'),
  ('C', 'Cancelled')
)

class Rsvp(models.Model):
  status = models.CharField(
    max_length=1,
    choices=RSVP_STATUS,
    default=RSVP_STATUS[0][0],
  )
  # email = models.EmailField()
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Dish(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=500)
  category = models.CharField(
    max_length=1,
    choices=DISH_CATEGORY,
    default=DISH_CATEGORY[0][0],
  )
  claimed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class Party(models.Model):
  name = models.CharField(max_length=100)
  owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  invite_id = models.CharField(max_length=6, unique=True, blank=True)
  rsvp = models.ForeignKey(Rsvp, on_delete=models.CASCADE)
  dishes = models.ForeignKey(Dish, on_delete=models.CASCADE)
  time = models.DateField()
  location = models.CharField(max_length=150)
  dresscode = models.CharField(max_length=100)
  status = models.CharField(
    max_length=1,
    choices=PARTY_STATUS,
    default=PARTY_STATUS[0][0],
  )
