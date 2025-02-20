from django import forms
from .models import Rsvp, Party
from django.forms import DateTimeInput

class RsvpForm(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = ['status']

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['name', 'time', 'location', 'dresscode']
        widgets = {
            'time': forms.DateTimeInput(
            # format=('%Y-%m-%d %H:%M'),
            attrs={
                'placeholder': 'Select a date',
                'type': 'datetime-local'
            }
        )
    }