import uuid

class Expense:
    def __init__(self, expense_id: str ,user_id: int, name: str, price: int, category: str):
        self.expense_id = expense_id if expense_id else str(uuid.uuid4())
        self.user_id = user_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self) -> str:
        return f"{self.name} - {self.price}$ in -{self.category}- category\n"

    def __repr__(self) -> str:
        return f"Expense(expense_id {self.expense_id}, user_id={self.user_id}, name='{self.name}', price={self.price}, category='{self.category}')"

    def to_file_line(self) -> str:
        return f"{self.expense_id};{self.user_id};{self.name};{self.price};{self.category}\n"


