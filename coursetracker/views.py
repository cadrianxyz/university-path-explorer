from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
from oakhacksvancoders.scrapers import ubcexplorer, ubcgrades, rmp

# the main dictionary
courseInfo = {}

# search works as a "buffer" for when we are obtaining data
def search(request):
    if request.method == 'GET':
        search = request.GET.get('find')
        # print('search', search)
        return redirect('coursetracker:course', pk=search)

def course(request, pk):
    # get the subject and number
    pkSplitted = pk.split(' ')
    if(len(pkSplitted) > 1):
        subject = pkSplitted[0].upper() 
        number = pkSplitted[1]
    else:
        subject = pk[0:-3].upper() 
        number = pk[-3:]
        if(not len(subject) <= 5 or not isinstance(subject, str) or not str.isdigit(number)):
            return render(request, 'coursetracker/404.html')

    # use the given id to do a prereq lookup (ubcexplorer)
    courseInfo = ubcexplorer.generateCoursePrereqTree(subject + " " + number)
    # ******
    # comment out line above if taking too long
    # ******

    # find out grade distribution (ubc grades)
    ## get the course sessions first
    courseSessions = ubcgrades.findCourseSessions(subject, number)
    distributions = {}
    print(courseSessions)
    for sesh in courseSessions:
        distributions[sesh] = ubcgrades.grade_distribution('2018W', subject, number, sesh)

    # temporary 'OVERALL'
    i = 0
    sesh = courseSessions[i]
    while not distributions[sesh]:
        i += 1
        sesh = courseSessions[i]

    courseInfo['distributions'] = list(distributions[sesh]['grades'].values())
    courseInfo['stats'] = { 'average': distributions[sesh]['average'],
                            'stdev': distributions[sesh]['stdev'],
                            'high': distributions[sesh]['high'],
                            'low': distributions[sesh]['low'],
                            'pass': distributions[sesh]['pass'],
                            'fail': distributions[sesh]['fail'],
                            'withdrew': distributions[sesh]['withdrew'],
                            'audit': distributions[sesh]['audit'],
                            'other': distributions[sesh]['other'] }

    try:
        instructorName = distributions[courseSessions[0]]['instructor'].split(', ')
        instructorName = instructorName[1] + " " + instructorName[0]
    except:
        instructorName = 'TBA'

    prof = rmp.UBCprofs.SearchProfessor(instructorName)
    courseInfo['instructor'] = {
        'name': instructorName,
        'overall rating': prof['rating_class'],
        'rating ': prof['overall_rating'],
        'number of ratings': prof['tNumRatings'],
    }
    # print(courseInfo)


    return render(request, 'coursetracker/course.html', { 'courseData': courseInfo })

class ClubChartView(TemplateView):
    template_name = 'coursetracker/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"]
        return context