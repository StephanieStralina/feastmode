from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from main_app.models import Party
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
    return render(request, 'parties/party-detail.html', { 'party': party })

class PartyCreate(LoginRequiredMixin, CreateView):
    model = Party
    fields = ['name', 'time', 'location', 'dresscode']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PartyUpdate(LoginRequiredMixin, UpdateView):
    model = Party
    fields = ['name', 'time', 'location', 'dresscode']

    def get_object(self,queryset= None):
        print(self.kwargs.get('invite_id'))
        return Party.objects.get(invite_id= self.kwargs.get('invite_id'))
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)