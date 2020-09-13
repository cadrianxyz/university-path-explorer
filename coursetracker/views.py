from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
from oakhacksvancoders.scrapers import ubcexplorer, ubcgrades
# Create your views here.

def home(request):
    return render(request, 'coursetracker/search.html')

def course(request, pk):
    # get the subject and number
    pkSplitted = pk.split(' ')
    if(len(pkSplitted) > 1):
        subject = pkSplitted[0]
        number = pkSplitted[1]
    else:
        subject = pk[0:-3]
        number = pk[-3:]
        print('subject', subject, isinstance(subject, str))
        print('number', number, str.isdigit(number))
        if(not isinstance(subject, str) or not str.isdigit(number)):
            return render(request, 'coursetracker/404.html')

    # course = Course.objects.get(id=pk)

    # use the given id to do a prereq lookup (ubcexplorer)
    courseInfo = ubcexplorer.generateCoursePrereqTree('ELEC 202')
    # ******
    # replace above line with the following (if taking too long)
    # courseInfo = {}
    # ******

    # find out course grade profile (ubc grades)
    courseInfo['grade_profile'] = ubcgrades.grade_profile(subject, number)

    # find out grade distribution (ubc grades)
    ## get the course sessions first
    courseSessions = ubcgrades.findCourseSessions(subject, number)
    distributions = {}
    for sesh in courseSessions:
        distributions[sesh] = ubcgrades.grade_distribution('2018W', 'ELEC', '202')

    return render(request, 'coursetracker/course.html', { 'courseData': courseInfo })

class ClubChartView(TemplateView):
    template_name = 'coursetracker/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"]
        return context