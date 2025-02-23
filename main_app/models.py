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

class Party(models.Model):
  name = models.CharField(max_length=100)
  owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  invite_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
  time = models.DateTimeField()
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
    return reverse('party-detail', kwargs={ 'invite_id': self.invite_id })

class Rsvp(models.Model):
  party = models.ForeignKey(Party, on_delete=models.CASCADE)
  status = models.CharField(
    max_length=1,
    choices=RSVP_STATUS,
    default=RSVP_STATUS[0][0],
  )
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

  def __str__(self):
    return f"{self.status} - {self.user.username} - {self.party.invite_id}"
  
class Dish(models.Model):
  party = models.ForeignKey(Party, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  img_url = models.URLField(max_length=300, verbose_name='Image URL')
  description = models.TextField(max_length=500)
  category = models.CharField(
    max_length=1,
    choices=DISH_CATEGORY,
    default=DISH_CATEGORY[0][0],
  )
  claimed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

  def __str__(self):
    return f"{self.name}"