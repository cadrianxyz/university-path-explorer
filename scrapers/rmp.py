import requests
import json
import math

## Professor Returned Information:
# tSid, tid - institution id, prof id
# institution_name
# tFname, tMiddlename, tLname
# tDept - department
# contentType - 'TEACHER'
# categoryType - 'PROFESSOR'
# tNumRatings - number of people who rated
# rating_class - 'good', 'bad', 'poor'
# overall_rating - average rating out of 5

## Use as below:
# from .scrapers.rmp import UBCprofs
# professor = UBCprofs.SearchProfessor("Robert Gateman")
# pass into view

class RMPScraper:
    def __init__(self, schoolid):
        self.UniversityId = schoolid
        self.professors = self.GetAllProfessors()
        self.professorIndex = False

    ## ----
    ## UTILITY FUNCTIONS
    ## ----

    # returns the number of professors in the university
    # arguments:
    # id - university id
    def GetProfessorCount(self, id):
        # opens the page
        page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(id))
        # gets the page in json
        page_json = json.loads(page.content)
        # get the number of professors (20 is displayed per page)
        num_of_profs = page_json['remaining'] + 20
        return num_of_profs

    # returns the professor's index
    # arguments:
    # query - the search string, professor's name
    def GetProfessorIndex(self, query):
        for p in range(0, len(self.professors)):
            if (query == (self.professors[p]['tFname'] + " " + self.professors[p]['tLname'])):
                return p
        return False

    # returns a list of all the professors
    # arguments: none
    def GetAllProfessors(self):
        professors_list = []
        num_of_profs = self.GetProfessorCount(self.UniversityId)
        num_of_pages = math.ceil(num_of_profs / 20)
        i = 1
        # the loop insert all professors into a list
        while (i <= num_of_pages):
            # opens each of the pages
            page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(i)
                + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(self.UniversityId))
            page_json = json.loads(page.content)
            page_profs = page_json['professors']
            # adds each professor to the list
            professors_list.extend(page_profs)
            i += 1
        return professors_list

    ## ----
    ## FUNCTIONS TO-USE
    ## ----

    # searches and returns the professor's details
    # arguments:
    # query - the search string
    def SearchProfessor(self, query):
        self.professorIndex = self.GetProfessorIndex(query)
        return self.professors[self.professorIndex]

    # returns the professor's specific detail
    # arguments:
    # key - the key of the detail
    def GetProfessorDetail(self, key):
        print(self.professors[self.professorIndex][key])
        return self.professors[self.professorIndex][key]


UBCprofs = RMPScraper(1413)

# Uni = RMPScraper(123)
# Uni.SearchProfessor("Robert Gatemam")
# Uni.PrintProfessorDetail("overall_rating")