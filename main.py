# Final CLI spending manager
from models import Expense
from storage import load_expense, save_expense, get_categories

#menu
print("""1 - Add spending
2 - Show all expenses
3 - Show the total amount
4 - Show expenses by category
5 - Exit""")

#Functions
while True:
    choice = input("\nChoose an action: ")

    match choice:
        case '1':
            print("Add spending")
            name = input("What you want to add?: ")
            price = int(input("price: "))
            category = input("What category is it?: ")

            expense = Expense(name, price, category)
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
            print("Program is finished, thanks for using me) \nBye")
            break

        case _:
            print("Wrong input")
