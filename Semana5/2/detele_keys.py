list_of_keys = ['access_level', 'age']

employee = {
    'name': 'Luis',
    'email': 'Cordero@ecorp.com',
    'access_level': 5,
    'age': 29
}

for key in list_of_keys:
    if key in employee:
        del employee[key]

print(employee)
