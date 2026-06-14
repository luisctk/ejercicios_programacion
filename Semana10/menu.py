from actions import inserting_student, show_all_students, show_average, top_students
from data import export_to_csv, import_from_csv, list_exported_files

def main_menu():
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
            insert_student()
            input("Press Enter to continue...")
        elif selection == 2:
            all_students()
            input("Press Enter to continue...")
        elif selection == 3:
            top_students()
            input("Press Enter to continue...")
        elif selection == 4:
            showing_total_average()
        elif selection == 5:
            print("\n--- EXPORT DATA ---")
            filename = input("File name (Enter for 'students_export.csv'): ")
            if filename.strip() == "":
                filename = "students_export.csv"
            export_to_csv(filename)
            input("Press Enter to continue...")
        elif selection == 6:
            print("\n--- IMPORT DATA ---")
            list_exported_files()
            filename = input("File name to import (Enter for 'students_export.csv'): ")
            if filename.strip() == "":
                filename = "students_export.csv"
            import_from_csv(filename)
            input("Press Enter to continue...")
        elif selection == 8:
            print('Bye Bye!')
            break
        else:
            print("Invalid option. Choose 1-6 or 8")
            input("Press Enter to continue...")

def insert_student():
    inserting_student()

def all_students():
    show_all_students()

def showing_total_average():
    while True:
        print("\n--- AVERAGE SUBMENU ---")
        print("1 = Spanish")
        print("2 = English")
        print("3 = Social")
        print("4 = Sciences")
        print("5 = Go to main menu")
        
        try:
            selection = int(input("Choose an option: "))
        except ValueError:
            print("Please enter a valid number (1-5)")
            continue
        
        if selection == 1:
            show_average(2)
            input("Press Enter to continue...")
        elif selection == 2:
            show_average(3)
            input("Press Enter to continue...")
        elif selection == 3:
            show_average(4)
            input("Press Enter to continue...")
        elif selection == 4:
            show_average(5)
            input("Press Enter to continue...")
        elif selection == 5:
            break
        else:
            print("Please choose from 1 to 5")