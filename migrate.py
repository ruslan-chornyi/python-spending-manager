import uuid

Old_format_lines = 4

def migrate():

    with open('data/expenses.json', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.split(',')

        if len(parts) == Old_format_lines:
            user_id, name, price, category = parts
            expense_id = uuid.uuid4()
            new_lines.append(f"{expense_id};{user_id};{name},{price},{category}")

        else:
            new_lines.append(line)

    with open('data/expenses.txt', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Migration was successful! \nNew lines: {len(new_lines)}")

if __name__ == "__main__":
    migrate()