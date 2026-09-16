# Final CLI spending manager
from models import Expense
from storage import load_expense, save_expense, get_categories, delete_expense
import uuid

Local_User_Id = 0

#menu
print("""1 - Add spending
2 - Show all expenses
3 - Show the total amount
4 - Show expenses by category
5 - delete
6 - Exit""")

#Functions
while True:
    choice = input("\nChoose an action: ")

    match choice:
        case '1':
            print("Add spending")
            name = input("What you want to add?: ")
            price = int(input("price: "))
            category = input("What category is it?: ")
            expense_id = str(uuid.uuid4())

            expense = Expense(expense_id ,Local_User_Id, name, price, category)
            save_expense(expense)

        case '2':
            print("Show all expenses")

            for e in load_expense():
                print(e, end='')

        case '3':
            print("Show the total amount")
            total = 0

            for e in load_expense():
                total += e.price
            print(f"Total amount = {total}$")

        case '4':
            print("Show expenses by category\n")
            expenses = load_expense()
            print(get_categories(expenses))
            user_category = input("What category you want to see?: ").lower()
            total = 0

            for e in expenses:
                if e.category == user_category:
                    print(f"{e.name} - {e.price}$ ({e.category})")
                    total += e.price

            print(f"\nTotal amount = {total}$")

        case '5':
            print("Delete expense")
            expenses = load_expense()
            ex_id = []

            for i, e in enumerate(expenses, start=1):
                ex_id.append(e.expense_id)
                print(i, '-', e, end='')

            user_input = input("Choose what you want to delete: ")

            if not user_input.isdigit():
                print("Wrong input")
            else:
                user_delete_num = int(user_input)
                if user_delete_num < 1 or user_delete_num > len(ex_id):
                    print("Number out of range")
                else:
                    selected_id = ex_id[user_delete_num - 1]
                    if delete_expense(selected_id):
                        print("Success!")
                    else:
                        print("ID not found")

        case '6':
            print("Program is finished, thanks for using me) \nBye")
            break

        case _:
            print("Wrong input")
