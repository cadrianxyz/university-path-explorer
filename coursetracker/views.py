from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
from oakhacksvancoders.scrapers import ubcexplorer
# Create your views here.

def home(request):
    return render(request, 'coursetracker/search.html')

def course(request, pk):
    # course = Course.objects.get(id=pk)

    # use the given id to do the lookup
    courseInfo = ubcexplorer.generateCoursePrereqTree('ELEC 202')
    # replace above line with the following (if taking too long) courseInfo = {}

    return render(request, 'coursetracker/course.html', { 'courseData': courseInfo })

class ClubChartView(TemplateView):
    template_name = 'coursetracker/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"]
        return context