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


# utc and alpha time zone are both ahead of PST by 8 hours
if __name__ == '__main__':
    # set api necessities and create canvas object
    API_URL = keys.URL
    API_KEY = keys.TOKEN
    canvas = cv.Canvas(API_URL, API_KEY)

    # gets courses & respective term. Returns dict -> course.term; 'name' is the key for the term name
    courses = canvas.get_courses(include=['term'])

    # Get current time & run it through function 'turnInToDTObj' - gets rid of milliseconds - keeps it as datetime obj
    now = str(datetime.now(dt.timezone.utc))
    nowDTObject = turnInToDTObj(now)

    # authenticates twilio account and creates client object
    client = Client(keys.TWILIO_ACCOUNT_SID, keys.TWILIO_AUTH_TOKEN)

    # go through each course and print each assignment and time left to submit
    for course in courses:
        # catch exception in case course isn't in current term or has no name
        try:
            if course.term['name'] == "Fall 2020 Semester" and course.name:
                print("For " + str(course) + ':')

                # this gets the upcoming assignments of a course (assignments whose due date hasn't passed)
                assignments = course.get_assignments(bucket="upcoming")
                for assignment in assignments:
                    try:
                        # checks if assignment is meant to be graded if it is then print
                        if assignment.points_possible > 0:
                            assignmentDTObject = turnInToDTObj(assignment.due_at)
                            timeLeft = str(assignmentDTObject - nowDTObject)
                            print("    Assignment: " + assignment.name + ", is due in: "
                                  + timeLeft)
                            # checks if assignment is due in less than 24 hours
                            if "day" not in timeLeft:
                                print("    This assignment is due today")
                                # this sends a text message informing the user that an assignment is due today
                                message = client.messages \
                                    .create(
                                        body="Hey, " + assignment.name + " is due today.",
                                        from_=keys.TWILIO_NUMBER,
                                        to=keys.USER_NUM
                                    )
                    except TypeError as er:
                        pass
                        # print("Error occurred, " + str(er))
                print()
        except AttributeError as e:
            pass
            # print("Error occurred, " + str(e))
