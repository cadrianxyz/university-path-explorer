from django.shortcuts import render
from .models import Genre

# Create your views here.
def show_genres(request):
    return render(request, "genres.html", {'genres': Genre.objects.all()})