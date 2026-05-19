import json

def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def display_type_options(valid_types):
    print("\n--- Available Pokemon Types ---")
    print(", ".join(valid_types))
    print("-------------------------------")

def get_pokemon_types():
    valid_types = [
        "Normal", "Fire", "Water", "Grass", "Electric", "Ice", 
        "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", 
        "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"
    ]
    types = []
    
    display_type_options(valid_types)
    
    while True:
        poke_type = input("\nEnter a type from the list (or 'done' to finish): ").strip().capitalize()
        
        if poke_type.lower() == 'done':
            if len(types) > 0:
                break
            else:
                print("You must enter at least one type.")
        elif poke_type in valid_types:
            if poke_type not in types:
                types.append(poke_type)
                print(f"Added! Current types: {', '.join(types)}")
            else:
                print("Type already added.")
        else:
            print("Invalid type. Please check the list and try again.")
            
    return types

def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Must be a number.")

def get_pokemon_data():
    name = input("Pokemon name: ")
    types = get_pokemon_types()
    
    print("\n--- Base Stats ---")
    hp = get_integer_input("HP: ")
    attack = get_integer_input("Attack: ")
    defense = get_integer_input("Defense: ")
    sp_attack = get_integer_input("Sp. Attack: ")
    sp_defense = get_integer_input("Sp. Defense: ")
    speed = get_integer_input("Speed: ")

    return {
        "name": {
            "english": name
        },
        "type": types,
        "base": {
            "HP": hp,
            "Attack": attack,
            "Defense": defense,
            "Sp. Attack": sp_attack,
            "Sp. Defense": sp_defense,
            "Speed": speed
        }
    }

def main():
    filename = "pokemon.json"
    pokemons = load_json(filename)
    
    new_pokemon = get_pokemon_data()
    pokemons.append(new_pokemon)
    
    save_json(pokemons, filename)
    print("\nPokemon added successfully!")

if __name__ == "__main__":
    main()