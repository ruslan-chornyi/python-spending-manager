from models import Expense

def load_expense():
    expenses = []
    with open("data/expenses.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            name, price, category = line.strip().split(';')
            category = category.lower()
            expenses.append(Expense(str(name), int(price), str(category)))
    return expenses

def save_expense(expense):
    with open("data/expenses.txt", 'a', encoding='utf-8') as f:
        f.write(expense.to_file_line())

def once_category(expenses):
    return {e.category for e in expenses}