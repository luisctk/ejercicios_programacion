class Flyer:
    def fly(self):
        return "Flying"
    
    def land(self):
        return "Landing"


class Swimmer:
    def swim(self):
        return "Swimming"
    
    def dive(self):
        return "Diving"


class Walker:
    def walk(self):
        return "Walking"
    
    def run(self):
        return "Running"


class Duck(Flyer, Swimmer, Walker):
    def __init__(self, name):
        self.name = name
    
    def describe(self):
        return f"{self.name} can: {self.fly()}, {self.swim()}, {self.walk()}"


class Penguin(Swimmer, Walker):
    def __init__(self, name):
        self.name = name
    
    def describe(self):
        return f"{self.name} can: {self.swim()}, {self.walk()} (but cannot fly)"


class Airplane(Flyer):
    def __init__(self, model):
        self.model = model
    
    def describe(self):
        return f"Airplane {self.model} can: {self.fly()}, {self.land()}"