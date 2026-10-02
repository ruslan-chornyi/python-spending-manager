from app.models import Expense
from app.storage import save_expense

Old_format_lines = 4

def migrate():
    with open('../data/expenses.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        parts = line.split(';')

        if len(parts) == Old_format_lines:
            user_id, name, price, category = parts
        else:
            expense_id, user_id, name, price, category = parts

        expense = Expense(user_id=int(user_id), name=name, price=int(price), category=category.strip())
        save_expense(expense)
        count += 1

    print(f"Migration was successful! \nTransferred: {count}")

if __name__ == "__main__":
    migrate()