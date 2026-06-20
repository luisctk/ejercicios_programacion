def inserting_student(students):
    name = input('Insert a name = ')
    section = input('Insert a section = ')
    spanish = spanish_grade()
    english = english_grade()
    social = social_grade()
    sciences = sciences_grade()
    
    student = {
        'name': name,
        'section': section,
        'spanish': spanish,
        'english': english,
        'social': social,
        'sciences': sciences
    }
    
    students.append(student)
    print(f"Estudiante {name} agregado correctamente")

def spanish_grade():
    while True:
        try:
            grade = int(input('Insert the spanish grade = '))
            if grade < 0:
                print('The grade needs to be greater or equal than 0')
            elif grade > 100:
                print('The max grade is 100')
            else:
                return grade
        except ValueError:
            print('Please enter a valid number (0-100)')

def english_grade():
    while True:
        try:
            grade = int(input('Insert the english grade = '))
            if grade < 0:
                print('The grade needs to be greater or equal than 0')
            elif grade > 100:
                print('The max grade is 100')
            else:
                return grade
        except ValueError:
            print('Please enter a valid number (0-100)')

def social_grade():
    while True:
        try:
            grade = int(input('Insert the social grade = '))
            if grade < 0:
                print('The grade needs to be greater or equal than 0')
            elif grade > 100:
                print('The max grade is 100')
            else:
                return grade
        except ValueError:
            print('Please enter a valid number (0-100)')

def sciences_grade():
    while True:
        try:
            grade = int(input('Insert the sciences grade = '))
            if grade < 0:
                print('The grade needs to be greater or equal than 0')
            elif grade > 100:
                print('The max grade is 100')
            else:
                return grade
        except ValueError:
            print('Please enter a valid number (0-100)')

def show_all_students(students):
    if len(students) == 0:
        print("No hay estudiantes registrados")
        return
    
    print("\n" + "="*60)
    print(f"{'Name':<20} {'Section':<10} {'Spanish':<8} {'English':<8} {'Social':<8} {'Sciences':<8}")
    print("="*60)
    
    for student in students:
        print(f"{student['name']:<20} {student['section']:<10} {student['spanish']:<8} {student['english']:<8} {student['social']:<8} {student['sciences']:<8}")
    print("="*60)

def top_students(students):
    if len(students) == 0:
        print("No hay estudiantes registrados")
        return
    
    students_with_avg = []
    
    for student in students:
        average = (student['spanish'] + student['english'] + student['social'] + student['sciences']) / 4
        students_with_avg.append((student['name'], student['section'], average))
    
    students_with_avg.sort(key=lambda x: x[2], reverse=True)
    
    print("\n" + "="*50)
    print("TOP 3 BEST STUDENTS")
    print("="*50)
    
    for i in range(min(3, len(students_with_avg))):
        name, section, avg = students_with_avg[i]
        print(f"{i+1}. {name} (Section: {section}) - Average: {avg:.2f}")
    
    print("="*50)