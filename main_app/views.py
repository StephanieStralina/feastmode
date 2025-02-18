from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from main_app.models import Party

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