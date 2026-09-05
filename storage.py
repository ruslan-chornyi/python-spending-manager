from models import Expense
import os

def load_expense() -> list[Expense]:

    if not os.path.exists("data/expenses.txt"):
        os.makedirs("data/expenses.txt")

    expenses = []
    with open("data/expenses.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            name, price, category = line.strip().split(';')
            category = category.lower()
            expenses.append(Expense(name, int(price), category))
    return expenses

def save_expense(expense) -> None:
    with open("data/expenses.txt", 'a', encoding='utf-8') as f:
        f.write(expense.to_file_line())

def get_categories(expenses: list[Expense]) -> set[str]:
    return {e.category for e in expenses}