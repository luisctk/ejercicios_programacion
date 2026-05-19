import csv


def write_csv(path):
    with open(path, 'a+', encoding='utf-8', newline='') as file:
                headers = ('name', 'gender', 'developer', 'clasification')
                data = []
                file.seek(0)
                first_char = file.read(1)
                file.seek(0, 2)  # volver al final
                writer = csv.DictWriter(file,headers, delimiter='\t')
                if not first_char:
                    writer.writeheader()  # ← escribir cabecera solo si archivo vacío
                while True:
                    try:
                        name = input('Give me the name: ')
                        gender = input('Give me the gender: ')
                        developer = input('Give me the developer: ')
                        clasification = int(input('Give me the clasification from 1 to 10: ' ))
                        new_game = {
                            'name': str(name),
                            'gender': str(gender),
                            'developer': str(developer),
                            'clasification': str(clasification)
                        }
                        data.append(new_game)
                        writer.writerow(new_game)
                        file.flush()
                        print('Game added!!')
                        exit_question = input('Do you want to add another game? Y/N ')
                        if exit_question == "N" or exit_question == "n":
                             break
                             
                    except ValueError:
                        print('error on clasification,please need to be a number')



write_csv('games_categorys_tabs.csv')