class Expense:
    def __init__(self, name: str, price: int, category: str):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self) -> str:
        return f"{self.name} - {self.price}$ in -{self.category}- category\n"

    def __repr__(self) -> str:
        return f"Expense(name='{self.name}', price={self.price}, category='{self.category}')"

    def to_file_line(self) -> str:
        return f"{self.name};{self.price};{self.category}\n"
