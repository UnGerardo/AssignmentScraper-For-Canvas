import canvasapi as cv
import datetime as dt
from datetime import datetime
import keys


# This method takes in a date and turns it into a datetime object to compare with others
def getDTInfo(datetimeDue):
    num = ''
    numList = []
    for char in datetimeDue:
        if char.isnumeric():
            num += char
        else:
            numList.append(int(num))
            num = ''
    return datetime(numList[0], numList[1], numList[2], numList[3], numList[4], numList[5])


if __name__ == '__main__':
    # set api necessities and create canvas object
    API_URL = keys.URL
    API_KEY = keys.TOKEN
    canvas = cv.Canvas(API_URL, API_KEY)

    # gets courses & respective term. Returns dict -> course.term; 'name' is the key for the term name
    courses = canvas.get_courses(include=['term'])

    
    now = str(datetime.now(dt.timezone.utc))
    nowDTObject = getDTInfo(now)
    # print('now = ' + now)

    for course in courses:
        try:
            if course.term['name'] == "Fall 2020 Semester" and course.name:
                print(str(course) + '\n')
                assignments = course.get_assignments(bucket="upcoming")
                for assignment in assignments:
                    try:
                        # assignment.due_at is printed in Alpha Time Zone format, need to convert to PST
                        # checks if assignment is meant to be graded if it is then print
                        if assignment.points_possible > 0:
                            print(assignment.name + ' ' + assignment.due_at)
                            assignmentDTObject = getDTInfo(assignment.due_at)
                            print(str(assignmentDTObject))
                            print(str(assignmentDTObject - nowDTObject))
                    except TypeError as er:
                        pass
                        # print("Error occurred, " + str(er))
                print()
        except AttributeError as e:
            pass
            # print("Error occurred, " + str(e))
