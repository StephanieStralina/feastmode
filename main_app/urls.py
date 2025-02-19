# main_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('parties/', views.party_index, name='party-index'),
    path('parties/create/', views.PartyCreate.as_view(), name='party-create'),
    path('parties/find/', views.party_find, name='party-find'),
    path('parties/<str:invite_id>/', views.party_detail, name='party-detail'),
    path('parties/<str:invite_id>/update/', views.PartyUpdate.as_view(), name='party-update'),
    path('parties/<str:invite_id>/add-rsvp/', views.add_rsvp, name='add-rsvp'),
    path('parties/<str:invite_id>/dishes/create/', views.DishCreate.as_view(), name='dish-create'),
    path('parties/<str:invite_id>/dishes/<int:pk>/update/', views.DishUpdate.as_view(), name='dish-update'),
] 