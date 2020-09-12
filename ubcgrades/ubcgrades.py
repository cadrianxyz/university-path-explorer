import requests

api = 'https://ubcgrades.com/api/'

# check if all methods do not equal 'None'

# methods for the drop down menus ---------------------

# returns all the sections of a course
def sections(term, subject, course):
    url = api + 'sections/' + term + '/' + subject + '/' + course
    r = requests.get(url)
    return r.json()

# returns all the courses for a subject
def courses(term, subject):
    url = api + 'courses/' + term + '/' + subject
    r = requests.get(url)
    return r.json()

# returns all the subjects for a term
def subjects(term):
    url = api + 'subjects/' + term
    r = requests.get(url)
    return r.json()

# returns all the terms
def years():
    url = api + 'yearsessions'
    r = requests.get(url)
    return r.json()

# -----------------------------------------------------------

# Methods for getting course details

# for getting grade profile of a course
# available keys: average, high, low, pass_percent
def grade_profile(subject, course):
    url = api + 'course-profile/' + subject + '/' + course
    r = requests.get(url)
    return r.json()

# for getting details from a section
# available keys: grades, stats, instructor, enrolled
        # available keys in grades: 0-9%, 10-19%, ... , 90-100%
        # available keys in stats: average, stdev, high, low, pass, fail,
                                # withdrew, audit, other
def grade_distribution(term, subject, course, section):
    url = api + 'grades/' + term + '/' + subject + '/' + course + '/' + section
    r = requests.get(url)
    if not r.json():
        return None
    else:
        return r.json()