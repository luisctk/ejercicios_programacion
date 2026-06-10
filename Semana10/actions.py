import menu
import csv

def inserting_student():
    name = input('Insert a name = ')
    section = input('Insert a section = ')
    spanish = spanish_grade()
    english = english_grade()
    social = social_grade()
    sciences = sciences_grade()
    saving_students(name, section,spanish , english, social, sciences)
    menu.main_menu()

def spanish_grade():
        while True:
            grade = int(input('Insert the spanish grade = '))
            try:
                if grade <= 0:
                    print('The grade need to be greater to 0')
                elif grade >= 100:
                    print('The max grade is 100')
                else:
                    return grade
            except ValueError as error:
                print(f'The value entered is no valid = {error}')

def english_grade():
        while True:
            grade = int(input('Insert the english grade = '))
            try:
                if grade <= 0:
                    print('The grade need to be greater to 0')
                elif grade >= 100:
                    print('The max grade is 100')
                else:
                    return grade
            except ValueError as error:
                print(f'The value entered is no valid = {error}')
                
def social_grade():
        while True:
            grade = int(input('Insert the social grade = '))
            try:
                if grade <= 0:
                    print('The grade need to be greater to 0')
                elif grade >= 100:
                    print('The max grade is 100')
                else:
                    return grade
            except ValueError as error:
                print(f'The value entered is no valid = {error}')

def sciences_grade():
        while True:
            grade = int(input('Insert the sciences grade = '))
            try:
                if grade <= 0:
                    print('The grade need to be greater to 0')
                elif grade >= 100:
                    print('The max grade is 100')
                else:
                    return grade
            except ValueError as error:
                print(f'The value entered is no valid = {error}')

def saving_students(name, section, spanish, english, social, sciences):
    with open('students.csv','a',newline='',encoding='utf-8') as file:
        fieldnames = ['name', 'section', 'spanish', 'english', 'social', 'sciences']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'name':name,
            'section':section,
            'spanish':spanish,
            'english':english,
            'social':social,
            'sciences':sciences,
        })
        print(f"Estudiante {name} guardado")


def show_all_students():
     with open('students.csv',"r",encoding='utf-8') as file:
          reader = csv.reader(file)

          next(reader)

          for read in reader:
               print(read)

def show_average(num_average):
     column = num_average
     value = 0
     with open('students.csv',"r",encoding='utf-8',newline='') as file:
          final_value = 0
          count = 0
          reader = csv.reader(file)
          average = 0
          next(reader)
          for read in reader:
               if len(read) > column:
                    count += 1 
                    value += int(read[column])
                    final_value = value
                    average = final_value / count

          
          print(f'The average is = {average}')      
                    

def top_students():
     with open('students.csv', 'r', newline='') as file:
          top_3 = []
          reader = csv.reader(file)
          next(reader)
          list_value = list(reader)
          for read in reader:
                if len(read) == 2:
                    spanish_grade_value = list_value[2]
                    english_grade_value = list_value[3]
                    social_grade_value = list_value[4]
                    sciences_grade_value = list_value[5]
                    count = 4
                    total_value = spanish_grade_value + english_grade_value + social_grade_value + sciences_grade_value / count
                    max(total_value)
                    print(total_value)            


        
        