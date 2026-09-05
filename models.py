class Expense:
    def __init__(self, user_id: int, name: str, price: int, category: str):
        self.user_id = user_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self) -> str:
        return f"{self.name} - {self.price}$ in -{self.category}- category\n"

    def __repr__(self) -> str:
        return f"Expense(user_id={self.user_id},name='{self.name}', price={self.price}, category='{self.category}')"

    def to_file_line(self) -> str:
        return f"{self.user_id};{self.name};{self.price};{self.category}\n"
