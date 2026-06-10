first_name = input('cual es tu nombre?')
last_name = input('cual es tu apellido?')
age = int(input('cual es tu edad?'))

if(age <= 2):
    print(f'Eres {first_name} {last_name} tu edad es {age} y eres un bebe')
elif(age >= 3 and age <= 9):
    print(f'Eres {first_name} {last_name} tu edad es {age} y eres un Infante')
elif(age >= 10 and age <= 12):
    print(f'Eres {first_name} {last_name} tu edad es {age} y eres un adolecente')
elif(age >= 13 and age <= 17):
    print(f'Eres {first_name} {last_name} tu edad es {age} y eres un adolecente') 
elif(age >= 18 and age <= 29):
    print(f'Eres {first_name} {last_name} tu edad es {age} y eres un Adulto joven')
elif(age >= 30 and age <= 59):
    print(f'Eres {first_name} {last_name} tu edad es {age} y eres un Adulto')
elif(age > 59):
    print(f'Eres {first_name} {last_name} tu edad es {age} y eres un Adulto mayor')