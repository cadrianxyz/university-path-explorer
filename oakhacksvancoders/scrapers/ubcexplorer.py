import requests

api = 'https://ubcexplorer.io/'
allCourseData = {}

# methods for finding course pre-requisites ---------------------

# returns all course data
def courses():
    url = api + 'getAllCourses/'
    r = requests.get(url)
    return r.json()

# returns all the courses for a subject
def courseInfo(code):
    url = api + 'getCourseInfo/' + code
    r = requests.get(url)
    try:
        response = r.json()
        return response
    except ValueError:
        return None

# returns the whole prerequisite tree for a subject, including course information
## course return form:
# {
#   "dept": "MATH",
#   "code": "MATH 100",
#   "name": "MATH",
#   "name": "Differential Calculus with Applications to Physical Sciences and Engineering",
#   "cred": 3,
#   "desc": "Derivatives of elementary functions. Applications and modelling: graphing, optimization. Consult the Faculty of Science Credit Exclusion List: www.calendar.ubc.ca/vancouver/index.cfm?tree=12,215,410,414. [3-0-0]",
#   "prer": "High-school calculus and one of (a) a score of 80% or higher in BC Principles of Mathematics 12 or Pre-calculus 12, or (b) a satisfactory score in the UBC Mathematics Basic Skills Test.",
#   "link": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept=MATH&course=100,
#   "creq": [],
#   "depn": [],
#   "preq": [], - will contain more course objects (nested)
# }
def generateCoursePrereqTree(code):
    # obtain information on the course
    course = courseInfo(code)
    # cache information so we don't need to query the same course
    allCourseData[code] = course

    preq = []
    if(course):
        for pr in course['preq']:
            # recursively obtain the same information for each prereq course
            if pr in allCourseData: # if not yet cached
                info = allCourseData[pr]
            else: # if already cached
                info = generateCoursePrereqTree(pr)
            preq.append(info)

        course['preq'] = preq
    
    return course
