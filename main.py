import canvasapi as cv
import keys

if __name__ == '__main__':
    API_URL = keys.URL
    API_KEY = keys.TOKEN

    canvas = cv.Canvas(API_URL, API_KEY)

    courses = canvas.get_courses(enrollment_status='active')

    for course in courses:
        try:
            print(course)
            assignments = course.get_assignments(bucket="upcoming")
            for assignment in assignments:
                try:
                    print(assignment)
                except AttributeError as er:
                    print("Error occurred, " + str(er))
            print()
        except AttributeError as e:
            print("Error occurred, " + str(e))