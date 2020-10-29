import canvasapi as cv
import keys

if __name__ == '__main__':
    API_URL = keys.URL
    API_KEY = keys.TOKEN

    canvas = cv.Canvas(API_URL, API_KEY)

    # gets all courses and includes the term of the course to check later. Results in a dict - course.term with the name
    # being the key for the term string
    courses = canvas.get_courses(include=['term'])

    for course in courses:
        try:
            if course.term['name'] == "Fall 2020 Semester" and course.name:
                print(course)
                assignments = course.get_assignments(bucket="upcoming")
                for assignment in assignments:
                    try:
                        # assignment.due_at is printed in Alpha Time Zone format, need to convert to PST
                        # checks if assignment is meant to be graded if it is then print
                        if assignment.points_possible > 0:
                            print(assignment.name + ' ' + assignment.due_at)
                    except TypeError as er:
                        pass
                        # print("Error occurred, " + str(er))
                print()
        except AttributeError as e:
            pass
            # print("Error occurred, " + str(e))
