class Person:
    def __init__(self, name):
        self.name = name

class Bus:
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
        self.passengers = []
    
    def add_passenger(self, person):
        if len(self.passengers) < self.max_passengers:
            self.passengers.append(person)
            print(f"{person.name} has boarded the bus.")
        else:
            print("The bus is full. Cannot add more passengers.")
    
    def remove_passenger(self, person):
        if person in self.passengers:
            self.passengers.remove(person)
            print(f"{person.name} has gotten off the bus.")
        else:
            print(f"{person.name} is not on the bus.")


max_pass = int(input("Insert the maximum number of passengers: "))
bus = Bus(max_pass)

while True:
    print("\n1. Add passenger")
    print("2. Remove passenger")
    print("3. Show passengers on the bus")
    print("4. Exit")
    
    option = input("Select an option: ")
    
    if option == "1":
        name = input("Insert the passenger name: ")
        person = Person(name)
        bus.add_passenger(person)
    
    elif option == "2":
        name = input("Insert the passenger name to remove: ")
        person = Person(name)
        bus.remove_passenger(person)
    
    elif option == "3":
        if len(bus.passengers) == 0:
            print("The bus is empty.")
        else:
            print("Passengers on the bus:")
            for p in bus.passengers:
                print(f"- {p.name}")
    
    elif option == "4":
        print("Goodbye!")
        break
    
    else:
        print("Invalid option. Please try again.")