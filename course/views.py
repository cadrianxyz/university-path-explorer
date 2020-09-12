from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from .models import *
# Create your views here.

def home(request):
    return render(request, 'course/chart.html')

def course(request, pk):
    course = Course.objects.get(id=pk)
    return render(request, 'course/course.html')

class ClubChartView(TemplateView):
    template_name = 'course/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"]
        return context