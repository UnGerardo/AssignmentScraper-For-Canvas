import canvasapi as cv
import datetime as dt
from datetime import datetime
import keys
from twilio.rest import Client


# This method takes in a date and turns it into a datetime object to compare with others
def turnInToDTObj(datetimeDue):
    num = ''
    numList = []
    for char in datetimeDue:
        if char.isnumeric():
            num += char
        else:
            numList.append(int(num))
            num = ''
    return datetime(numList[0], numList[1], numList[2], numList[3], numList[4], numList[5])


# utc and alpha time zone are both ahead of PST by 8 hours / maybe also check if assignments have started already
if __name__ == '__main__':
    # set api necessities and create canvas object
    API_URL = keys.URL
    API_TOKEN = keys.TOKEN
    canvas = cv.Canvas(API_URL, API_TOKEN)

    # create second canvas object if user has two different Canvas accounts
    SEC_API_URL = keys.SECOND_URL
    SEC_API_TOKEN = keys.SECOND_TOKEN
    secondCanvas = cv.Canvas(SEC_API_URL, SEC_API_TOKEN)

    # gets courses & respective term. Returns dict -> course.term; 'name' is the key for the term name
    courses = canvas.get_courses(include=['term'])
    secondCourses = secondCanvas.get_courses(include=['term'])
    allCourses = []

    # puts all courses in allCourses to only check one list
    for course in courses:
        allCourses.append(course)
    for course in secondCourses:
        allCourses.append(course)

    # Get current time & run it through function 'turnInToDTObj' - gets rid of milliseconds - keeps it as datetime obj
    now = str(datetime.now(dt.timezone.utc))
    nowDTObject = turnInToDTObj(now)

    # authenticates twilio account and creates client object
    client = Client(keys.TWILIO_ACCOUNT_SID, keys.TWILIO_AUTH_TOKEN)

    # collects every assignment that is due today to send one message with all of them
    assignmentsDueToday = []

    # go through each course and print each assignment and time left to submit
    for course in allCourses:
        # catch exception in case course isn't in current term or has no name
        try:
            if 'Fall 2020' in course.term['name'] and course.name:
                print("For " + str(course) + ':')

                # this gets the upcoming assignments of a course (assignments whose due date hasn't passed)
                assignments = course.get_assignments(bucket="upcoming")
                #print([ a for a in assignments]) #for POL-1 check discussion_topic dict and 'published' key and subscribed; check if any discussions are graded
                for assignment in assignments:
                    try:
                        # checks if assignment gives points and hasn't been submitted
                        if assignment.points_possible > 0 and not assignment.in_closed_grading_period:
                            # check if assignment is a discussion topic
                            if assignment.submission_types == ['discussion_topic']:
                                if assignment.subscribed:
                                    assignmentDTObject = turnInToDTObj(assignment.due_at)
                                    timeLeft = str(assignmentDTObject - nowDTObject)
                                    print("    Assignment: " + assignment.name + ", is due in: " + timeLeft)
                                    # checks if assignment is due in less than 24 hours
                                    if "day" not in timeLeft:
                                        print("    This assignment is due today")
                                        assignmentsDueToday.append(assignment.name)
                            else:
                                assignmentDTObject = turnInToDTObj(assignment.due_at)
                                timeLeft = str(assignmentDTObject - nowDTObject)
                                print("    Assignment: " + assignment.name + ", is due in: " + timeLeft)
                                # checks if assignment is due in less than 24 hours
                                if "day" not in timeLeft:
                                    print("    This assignment is due today")
                                    assignmentsDueToday.append(assignment.name)
                    except TypeError as er:
                        pass
                        # print("Error occurred, " + str(er))
                print()
        except AttributeError as e:
            pass
            # print("Error occurred, " + str(e))
        
    # this sends a text message informing the user that an assignment/s is due today
    if assignmentsDueToday:
        message = client.messages \
            .create(
                body=" \nDue today:\n" + ',\n'.join(assignmentsDueToday),
                from_=keys.TWILIO_NUMBER,
                to=keys.USER_NUM
            )
