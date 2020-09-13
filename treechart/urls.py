from django.urls import path
from .views import create_chart

urlpatterns = [
    path('', create_chart),
]