import csv
import os

def export_to_csv(filename="students_export.csv"):
    try:
        if not os.path.exists('students.csv'):
            print("No hay datos para exportar. Primero agrega estudiantes.")
            return False
        
        with open('students.csv', 'r', encoding='utf-8') as original:
            reader = csv.reader(original)
            datos = list(reader)
        
        if len(datos) <= 1:
            print("No hay estudiantes para exportar.")
            return False
        
        with open(filename, 'w', newline='', encoding='utf-8') as export_file:
            writer = csv.writer(export_file)
            writer.writerows(datos)
        
        print(f"Datos exportados exitosamente a '{filename}'")
        print(f"Total de estudiantes exportados: {len(datos) - 1}")
        return True
        
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False

def import_from_csv(filename="students_export.csv"):
    try:
        if not os.path.exists(filename):
            print(f"No se encuentra el archivo '{filename}'")
            print("Sugerencia: Primero exporta datos con la opcion 5")
            return False
        
        with open(filename, 'r', encoding='utf-8') as import_file:
            reader = csv.reader(import_file)
            datos_importados = list(reader)
        
        if len(datos_importados) <= 1:
            print("El archivo esta vacio o solo tiene encabezados.")
            return False
        
        expected_headers = ['name', 'section', 'spanish', 'english', 'social', 'sciences']
        headers = datos_importados[0]
        headers_lower = [h.lower().strip() for h in headers]
        
        if not all(h in headers_lower for h in expected_headers):
            print("El archivo no tiene el formato esperado.")
            print(f"Encabezados esperados: {expected_headers}")
            print(f"Encabezados encontrados: {headers}")
            respuesta = input("Deseas importar de todas formas? (s/n): ")
            if respuesta.lower() != 's':
                return False
        
        print("Opciones de importacion")
        print("1. Sobrescribir datos actuales")
        print("2. Combinar con datos existentes (evitar duplicados)")
        
        opcion = input("Elige una opcion (1 o 2): ")
        
        if opcion == "1":
            with open('students.csv', 'w', newline='', encoding='utf-8') as dest:
                writer = csv.writer(dest)
                writer.writerows(datos_importados)
            print(f"Datos importados. {len(datos_importados)-1} estudiantes cargados.")
            
        elif opcion == "2":
            datos_existentes = []
            if os.path.exists('students.csv'):
                with open('students.csv', 'r', encoding='utf-8') as existing:
                    reader = csv.reader(existing)
                    datos_existentes = list(reader)
            
            if len(datos_existentes) == 0:
                with open('students.csv', 'w', newline='', encoding='utf-8') as dest:
                    writer = csv.writer(dest)
                    writer.writerows(datos_importados)
            else:
                existing_names = set()
                for row in datos_existentes[1:]:
                    if len(row) > 0:
                        existing_names.add(row[0].lower())
                
                nuevos_estudiantes = []
                for row in datos_importados[1:]:
                    if len(row) > 0 and row[0].lower() not in existing_names:
                        nuevos_estudiantes.append(row)
                    elif len(row) > 0:
                        print(f"Estudiante '{row[0]}' ya existe, omitiendo...")
                
                if nuevos_estudiantes:
                    with open('students.csv', 'a', newline='', encoding='utf-8') as dest:
                        writer = csv.writer(dest)
                        writer.writerows(nuevos_estudiantes)
                    print(f"{len(nuevos_estudiantes)} nuevos estudiantes importados")
                else:
                    print("No se encontraron estudiantes nuevos para importar")
        else:
            print("Opcion invalida. Importacion cancelada.")
            return False
        
        return True
        
    except Exception as e:
        print(f"Error al importar: {e}")
        return False

def list_exported_files():
    try:
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        if csv_files:
            print("Archivos CSV disponibles:")
            for f in csv_files:
                size = os.path.getsize(f)
                print(f"   {f} ({size} bytes)")
        else:
            print("No hay archivos CSV en el directorio actual")
        return csv_files
    except Exception as e:
        print(f"Error al listar archivos: {e}")
        return []