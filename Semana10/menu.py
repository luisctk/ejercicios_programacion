from actions import inserting_student, show_all_students, top_students
from data import export_to_csv, import_from_csv

def main_menu(students):
    while True:
        print('\n' + '='*40)
        print('Thanks for using the Lyfter students system!')
        print('='*40)
        print("1 = Introduce a new student")
        print("2 = See all the students")
        print("3 = Top 3 best students")
        print("4 = See the note's average")
        print("5 = Export actual data")
        print("6 = Import exterior data")
        print("8 = To Exit")
        print('='*40)
        
        try:
            selection = int(input("Please select one option: "))
        except ValueError:
            print("Please enter a valid number (1-6 or 8)")
            input("Press Enter to continue...")
            continue
        
        if selection == 1:
            inserting_student(students)
            input("Press Enter to continue...")
        elif selection == 2:
            show_all_students(students)
            input("Press Enter to continue...")
        elif selection == 3:
            top_students(students)
            input("Press Enter to continue...")
        elif selection == 4:
            show_general_average(students)
            input("Press Enter to continue...")
        elif selection == 5:
            export_to_csv(students)
            input("Press Enter to continue...")
        elif selection == 6:
            import_from_csv(students)
            input("Press Enter to continue...")
        elif selection == 8:
            print('Bye Bye!')
            break
        else:
            print("Invalid option. Choose 1-6 or 8")
            input("Press Enter to continue...")

def show_general_average(students):
    if len(students) == 0:
        print("No hay estudiantes registrados")
        return
    
    total_general = 0
    for student in students:
        promedio = (student['spanish'] + student['english'] + student['social'] + student['sciences']) / 4
        total_general += promedio
    
    promedio_general = total_general / len(students)
    print(f"El promedio general de todos los estudiantes es: {promedio_general:.2f}")