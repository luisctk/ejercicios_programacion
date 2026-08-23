import csv
import os
from actions import Student

def export_to_csv(students):
    if len(students) == 0:
        print("No hay estudiantes para exportar")
        return False
    
    filename = input("Nombre del archivo (Enter para 'students_export.csv'): ")
    if filename.strip() == "":
        filename = "students_export.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['name', 'section', 'spanish', 'english', 'social', 'sciences']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for student in students:
                writer.writerow({
                    'name': student.name,
                    'section': student.section,
                    'spanish': student.spanish,
                    'english': student.english,
                    'social': student.social,
                    'sciences': student.sciences
                })
        
        print(f"Datos exportados a {filename}")
        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False

def import_from_csv(students):
    filename = input("Nombre del archivo a importar (Enter para 'students_export.csv'): ")
    if filename.strip() == "":
        filename = "students_export.csv"
    
    if not os.path.exists(filename):
        print(f"No se encuentra el archivo {filename}")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            imported = list(reader)
        
        if len(imported) == 0:
            print("El archivo esta vacio")
            return False
        
        for data in imported:
            student = Student(
                data['name'],
                data['section'],
                int(data['spanish']),
                int(data['english']),
                int(data['social']),
                int(data['sciences'])
            )
            students.append(student)
        
        print(f"{len(imported)} estudiantes importados correctamente")
        return True
    except Exception as e:
        print(f"Error al importar: {e}")
        return False