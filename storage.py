from models import Expense
import os

def load_expense() -> list[Expense]:

    if not os.path.exists("data/expenses.txt"):
        os.makedirs("data/expenses.txt")

    expenses = []
    with open("data/expenses.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            expense_id, user_id, name, price, category = line.strip().split(';')
            category = category.lower()
            expenses.append(Expense(str(expense_id), int(user_id), name, int(price), category))
    return expenses

def load_expense_by_user(user_id: int) -> list[Expense]:
    expenses = load_expense()
    return [e for e in expenses if e.user_id == user_id]

def save_expense(expense) -> None:
    with open("data/expenses.txt", 'a', encoding='utf-8') as f:
        f.write(expense.to_file_line())

def get_categories(expenses: list[Expense]) -> set[str]:
    return {e.category for e in expenses}

def delete_expense(expense_id: str) -> bool:
    expense = load_expense()
    remaining = [e for e in expense if e.expense_id != expense_id]

    if len(remaining) == len(expense):
        return False    #do nothing, if it didn`t find the id

    with open("data/expenses.txt", 'w', encoding='utf-8') as f:
        for e in remaining:
            f.write(e.to_file_line())
    return True
