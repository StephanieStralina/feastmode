from django.contrib import admin
from .models import Party, Dish, Rsvp


# Register your models here.
admin.site.register(Party)
admin.site.register(Dish)
admin.site.register(Rsvp)
