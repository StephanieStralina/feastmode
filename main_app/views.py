from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from main_app.models import Party, Rsvp
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RsvpForm

# Create your views here.

class Home(LoginView):
    template_name = 'home.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def party_index(request):
    parties = Party.objects.filter(owner=request.user)
    return render(request, 'parties/index.html', { 'parties': parties })

def party_detail(request, invite_id):
    party = Party.objects.get(invite_id=invite_id)
    rsvp_form = RsvpForm()
    return render(request, 'parties/party-detail.html', { 'party': party, 'rsvp_form': rsvp_form })

class PartyCreate(LoginRequiredMixin, CreateView):
    model = Party
    fields = ['name', 'time', 'location', 'dresscode']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PartyUpdate(LoginRequiredMixin, UpdateView):
    model = Party
    fields = ['name', 'time', 'location', 'dresscode']

    def get_object(self, queryset=None):
        return Party.objects.get(invite_id=self.kwargs.get('invite_id'))
    
def party_find(request):
    invite_id = request.GET.get('invite_id')
    return redirect('party-detail', invite_id=invite_id)

def add_rsvp(request, invite_id):
    rsvp_form = RsvpForm(request.POST)
    if rsvp_form.is_valid():
        party = Party.objects.get(invite_id=invite_id)
        existing_rsvp = None
        try:
            existing_rsvp = party.rsvp.get(user_id=request.user.id)
            if existing_rsvp:
                existing_rsvp.status = rsvp_form.cleaned_data['status']
                existing_rsvp.save()
        except Rsvp.DoesNotExist:
            new_rsvp = rsvp_form.save(commit=False)
            new_rsvp.user_id = request.user.id
            new_rsvp.save()
            party.rsvp.add(new_rsvp.id)

    return redirect('party-detail', invite_id=invite_id)
