# Final CLI spending manager
#menu
print("""1 - Add spending
2 - Show all expenses
3 - Show the total amount
4 - Show expenses by category
5 - Exit""")

def load_expenses():
    expenses = []
    with open("data/expenses.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            name, price, category = line.strip().lower().split(';')
            try:
                price = int(price)
            except ValueError:
                continue
            expenses.append((name, price, category))
    return expenses

while True:
    choiсe = input("\nChoose an action: ")

    match choiсe:
        case '1':
            print("Add spending")
            name = input("What you want to add?: ")
            price = input("How much it`s cost?: ")
            category = input("What category is it?: ")
            with open("data/expenses.txt", 'a', encoding='utf-8') as f:
                f.write(f"{name};{price};{category}\n")

        case '2':
            print("Show all expenses")
            for name, price, category in load_expenses():
                print(f"{name} - {price}$ ({category})")

        case '3':
            print("Show the total amount")
            total = 0
            for name, price, category in load_expenses():
                total += price
            print(f"Total amount = {total}$")

        case '4':
            print("Show expenses by category\n")
            user_category = input("What category you want to see?: ").lower()
            total = 0
            for name, price, category in load_expenses():
                if category == user_category:
                    print(f"{name} - {price}$ ({category})")
                    total += price

            print(f"\nTotal amount = {total}$")

        case '5':
            print("Program is finished, thanks for using me) \nBye")
            break

        case _:
            print("Wrong input")
