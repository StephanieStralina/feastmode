from django import forms
from .models import Rsvp, Party
from django.forms import DateTimeInput
from django.contrib.auth.forms import UserCreationForm

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

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters only.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters only.')
    email = forms.EmailField(required=True, help_text='Required. Letters, digits and @/./+/-/_ only.')

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')




