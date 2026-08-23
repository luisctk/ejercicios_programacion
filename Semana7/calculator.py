
def start():
    actual_number = 0
    try: 
        actual_number = int(input('Give me just one number to start '))
        actual_number = ask_numer(actual_number)
        return actual_number
        
        
    except ValueError:
        print('Debe ser un numero')
        start()

def ask_numer(actual_number):
    while True:
            try:
                question = int(input(f'what kind of operation do u wanna do? 1.Addition 2.Subtraction 3.Multiplication 4.Division 5.Borrar Numero Actual : {actual_number} -> '))
                if question == 1:
                    actual_number = addition(actual_number)
                elif question == 2:
                    actual_number = subtraction(actual_number)
                elif question == 3:
                    actual_number = multiplication(actual_number)
                elif question == 4:
                    if actual_number == 0:
                        raise ZeroDivisionError
                    else:
                        actual_number = division(actual_number)
                elif question == 5:
                    actual_number = clear_global_numer(actual_number)
                elif question >= 6:
                    raise ValueError
            
            except ValueError:
                print(f'Introcuce un numero del 1 al 4 (5 Para borrar el resultado actual)')
                actual_number = ask_numer(actual_number)
            
            except ZeroDivisionError:
                print('No puedes dividir entre 0')
                start()
    
def addition(actual_number):
    try:
        plus = int(input('Dame un numero para sumar'))
        print(f'Estas multiplicando {actual_number} + {plus}')
        actual_number = plus + actual_number
        print(f'El resultado de la suma es {actual_number}')
        return actual_number
    
    except ValueError as error:
        print(f'Debes introducir un numero {error}')
        start()


def subtraction(actual_number):
    try:
        sub1 = int(input('Dame un numero para restar'))
        print(f'Estas restando {actual_number} - {sub1}')
        actual_number = actual_number - sub1 
        print(f'El resultado de la resta es {actual_number}')
        return actual_number
    
    except ValueError as error:
        print(f'Debes introducir un numero {error}')
        start()


def multiplication(actual_number):
    try:
        mul1 = int(input('Dame un numero para multiplicar'))
        print(f'Estas multiplicando {actual_number} * {mul1}')
        actual_number = actual_number * mul1
        print(f'El resultado de la multiplicacion es {actual_number}')
        return actual_number
    
    except ValueError as error:
        print(f'Debes introducir un numero {error}')
        start()

def division(actual_number):
    try:
        mul1 = int(input('Dame un numero para dividir'))
        print(f'Estas dividiendo {actual_number} / {mul1}')
        actual_number = actual_number / mul1
        print(f'El resultado de la divicion es {actual_number}')
        return actual_number
    
    except ZeroDivisionError as error:
        print(f'NO PUEDES DIVIDIR ENTRE CERO {error}')
        start()

def clear_global_numer(actual_number):
    actual_number == 0
    print('Tu numero actual ahora es 0')
    start()



def main():
    try:
        start() 

    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()


                 