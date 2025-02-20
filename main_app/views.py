from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from django.urls import reverse
from main_app.models import Party, Rsvp, Dish
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RsvpForm
from .helpers import get_rsvp

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
    if request.user:
        rsvp = get_rsvp(party, request.user.id) 
    
    rsvp_form = RsvpForm(initial={ 'status': rsvp.status } if rsvp else {})
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
        existing_rsvp = get_rsvp(party, request.user.id)
        if existing_rsvp:
            existing_rsvp.status = rsvp_form.cleaned_data['status']
            existing_rsvp.save()
        else:
            new_rsvp = rsvp_form.save(commit=False)
            new_rsvp.user_id = request.user.id
            new_rsvp.party_id = party.id
            new_rsvp.save()

    return redirect('party-detail', invite_id=invite_id)

class DishCreate(LoginRequiredMixin, CreateView):
    model = Dish
    fields = ['name', 'description', 'category', 'claimed_by']

    def dispatch(self, request, *args, **kwargs):
        self.invite_id = kwargs['invite_id']
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.party = Party.objects.get(invite_id=self.invite_id)
        return super().form_valid(form)
    
    
    def get_success_url(self, **kwargs):
        return reverse('party-detail', kwargs={ 'invite_id': self.invite_id })

class DishUpdate(LoginRequiredMixin, UpdateView):
    model = Dish
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        self.invite_id = kwargs['invite_id']
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse('party-detail', kwargs={ 'invite_id': self.invite_id })

class DishDelete(LoginRequiredMixin, DeleteView):
    model = Dish
    
    def dispatch(self, request, *args, **kwargs):
        self.invite_id = kwargs['invite_id']
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self, **kwargs):
        return reverse('party-detail', kwargs={ 'invite_id': self.invite_id })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party'] = self.object.party
        return context

def dish_detail(request, dish_id, invite_id):
    dish = Dish.objects.get(id=dish_id)
    party = Party.objects.get(invite_id=invite_id)
    return render(request, 'parties/dish-detail.html', { 'dish': dish, 'party': party })