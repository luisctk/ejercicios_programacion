list_a = ['first_name', 'last_name', 'role']
list_b = ['Luis', 'Cordero', 'Software Engineer']

result = {}

for item in range(len(list_a)):
    result[list_a[item]] = list_b[item]

print(result)
