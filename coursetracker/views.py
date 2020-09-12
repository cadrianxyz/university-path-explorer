from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
# Create your views here.

def home(request):
    return render(request, 'coursetracker/search.html')

def course(request, pk):
    course = Course.objects.get(id=pk)
    return render(request, 'coursetracker/course.html')

class ClubChartView(TemplateView):
    template_name = 'coursetracker/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"]
        return context