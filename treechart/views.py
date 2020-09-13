from django.shortcuts import render
from .models import Chart

# Create your views here.

def create_chart(request):
    return render(request, "genres.html", {'charts': Chart.objects.all()})
