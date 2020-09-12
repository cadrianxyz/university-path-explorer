from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('course/<str:pk>', views.course),
]