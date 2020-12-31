import requests, json

api = 'https://ubcgrades.com/api/v1/'

# check if all methods do not equal 'None'
DEFAULT_TERM_SUMMER = '2018S'
DEFAULT_TERM_WINTER = '2018W'

# methods for the drop down menus ---------------------

# returns all the sections of a course
def sections(term, subject, course):
    url = api + 'sections/UBCV/' + term + '/' + subject + '/' + course
    r = requests.get(url)
    return r.json()

# returns all the courses for a subject
def courses(term, subject):
    url = api + 'courses/UBCV/' + term + '/' + subject
    r = requests.get(url)
    return r.json()

# returns all the subjects for a term
def subjects(term):
    url = api + 'subjects/UBCV/' + term
    r = requests.get(url)
    return r.json()

# returns all the terms
def years():
    url = api + 'yearsessions/UBCV'
    r = requests.get(url)
    return r.json()

# -----------------------------------------------------------

# Methods for getting course details

# for getting details from a section
# available keys: grades, stats, instructor, enrolled
        # available keys in grades: 0-9%, 10-19%, ... , 90-100%
        # available keys in stats: average, stdev, high, low, pass, fail,
                                # withdrew, audit, other
def grade_distribution(term, subject, course, section):
    url = api + 'grades/UBCV/' + term + '/' + subject + '/' + course + '/' + section
    return check_json(requests.get(url).json())

def findCourseSessions(subject, course):
    url = api + 'sections/UBCV/' + DEFAULT_TERM_SUMMER + '/' + subject + '/' + course
    r1 = check_json(requests.get(url).json())

    url = api + 'sections/UBCV/' + DEFAULT_TERM_WINTER + '/' + subject + '/' + course
    r2 = check_json(requests.get(url).json())
    
    if not r1:
        return r2
    elif not r2:
        return r1
    else:
        return r1 + r2

def get_rmp_details(subject, course):
    sect = sections(DEFAULT_TERM_WINTER, subject, course)
    instructors = {}
    for section in sect:
        instructor = grade_distribution(DEFAULT_TERM_WINTER, subject, course, section)['instructor'].split(', ')
        if len(instructor) > 1:
            instructor_name = instructor[1] + ' ' + instructor[0]
            
        section_num = grade_distribution(DEFAULT_TERM_WINTER, subject, course, section)['section']
            
        instructors[section_num] = instructor_name
    return instructors

def check_json(j):
    if 'error' in json.dumps(j):
        return []
    else:
        return j