from django.urls import path
from .views import matches_view
from . import views

urlpatterns = [
    path('', matches_view, name='matches'),
    path('search/', views.search, name="search"),
]
