from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.urls import reverse

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
  # party = models.ForeignKey(Party, on_delete=models.DO_NOTHING)

  def __str__(self):
    return f"{self.status} - {self.user.email}"

class Dish(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=500)
  category = models.CharField(
    max_length=1,
    choices=DISH_CATEGORY,
    default=DISH_CATEGORY[0][0],
  )
  claimed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

  def __str__(self):
    return f"{self.name}"

class Party(models.Model):
  name = models.CharField(max_length=100)
  owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  invite_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
  rsvp = models.ManyToManyField(Rsvp, blank=True)
  dishes = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=True, null=True)
  time = models.DateField()
  location = models.CharField(max_length=150)
  dresscode = models.CharField(max_length=100)
  status = models.CharField(
    max_length=1,
    choices=PARTY_STATUS,
    default=PARTY_STATUS[0][0],
  )

  def save(self, *args, **kwargs):
    if not self.invite_id:
      self.invite_id = str(uuid4())[:6]
      
    super().save(*args, **kwargs)

  def __str__(self):
    return f"{self.name}"
  
  def get_absolute_url(self):
    # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
    return reverse('party-detail', kwargs={ 'invite_id': self.invite_id })
