def read_and_sorte(path):
    with open(path,'r', encoding='utf-8') as file:
        list_sorted = file.readlines()
        for songs in list_sorted:
            print(songs)

        list_sorted.sort()
            

    with open('songs_sorted.txt','w',encoding='utf-8') as file:
        file.writelines(list_sorted)
        print('List updated')


read_and_sorte('songs.txt')