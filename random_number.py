import random

random_int = random.randint(0, 10)
guessed = False  # 'adivinado' ahora es 'guessed'

while (not guessed):
    ask_number = int(input('Dame un numero del 1 al 10'))
    
    if (ask_number != random_int):
        print('intentalo de nuevo')
    else:
        guessed = True
        print('Lo lograste')