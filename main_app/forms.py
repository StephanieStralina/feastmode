from django import forms
from .models import Rsvp

class RsvpForm(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = ['status']