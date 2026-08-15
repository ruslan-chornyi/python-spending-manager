class Expense:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"{self.name} - {self.price}$ in -{self.category}- category\n"

    def __repr__(self):
        return f"Expense(name='{self.name}', price={self.price}, category='{self.category}')"

    def to_file_line(self):
        return f"{self.name} - {self.price}$ ({self.category})\n"