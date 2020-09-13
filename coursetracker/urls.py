from django.urls import path
from . import views

app_name = 'coursetracker'

urlpatterns = [
    path('search', views.search, name="search"),
    path('view/<str:pk>', views.course, name="course")
] 