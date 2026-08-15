import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def get_area(self):
        return math.pi * self.radius ** 2


while True:
    try:
        radio = float(input("Insert the radius of the circle (or 0 to exit): "))
        if radio == 0:
            print("Goodbye!")
            break
        circle = Circle(radio)
        area = circle.get_area()
        print(f"The area of the circle is: {area:.2f}")
    except ValueError:
        print("Please enter a valid number.")