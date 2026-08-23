grades = [55, 79, 74, 65, 66]
passed_count = 0
failed_count = 0
total = 0
passed_sum = 0
failed_sum = 0

for grade in grades:
    if grade > 70:
        passed_count += 1
        passed_sum += grade
        print(f'{passed_sum}')
    elif grade < 70:
        failed_count += 1
        failed_sum += grade
        print(f'{failed_sum}')
    elif grade == 0:
        print('It is 0 buddy') 

for grade_sum in grades:
    total += grade_sum

total_average = total / len(grades)

# Aquí está tu if lineal aplicado a ambos para seguridad
passed_average = (passed_sum / passed_count) if passed_count > 0 else 0
failed_average = (failed_sum / failed_count) if failed_count > 0 else 0

print(f'Total passed grades = {passed_count}')
print(f'Total failed grades = {failed_count}')
print(f'Total average = {total_average}')
print(f'Average of passed grades = {passed_average}')
print(f'Average of failed grades = {failed_average}')