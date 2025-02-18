# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('parties/', views.party_index, name='party-index'),
    path('parties/create/', views.PartyCreate.as_view(), name='party-create'),
    path('parties/<str:invite_id>/', views.party_detail, name='party-detail'),
   
]