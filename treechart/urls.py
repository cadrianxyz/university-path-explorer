from django.urls import path
from .views import show_genres

urlpatterns = [
    path('', show_genres),
]