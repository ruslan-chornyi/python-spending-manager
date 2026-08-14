class Expense:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"{self.name} - {self.price}$ in {self.category} category\n"

    def to_file_line(self):
        return f"{self.name} - {self.price}$ ({self.category})\n"


list = []

while True:
    name = input("\nEnter a name or 'stop' to finish: ")
    if name.lower() == "stop":
        break
    price = int(input("Price: "))
    category = input("Category: ")

    list.append(Expense(name, price, category))

print("\nAll expenses:")
for e in list:
    print(e, end='')

