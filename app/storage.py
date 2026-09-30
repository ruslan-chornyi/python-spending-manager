from app.db import Base, engine, SessionLocal
from app.models import Expense


def init_db() -> None:
    Base.metadata.create_all(engine)

def save_expense(expense: Expense) -> None:
    expense.category = expense.category.lower()
    with SessionLocal() as session:
        session.add(expense)
        session.commit()

def load_expense() -> list[Expense]:
    with SessionLocal() as session:
        return session.query(Expense).all()

def load_expense_by_user(user_id: int) -> list[Expense]:
    with SessionLocal() as session:
        return session.query(Expense).filter(Expense.user_id == user_id).all()

def get_categories(expenses: list[Expense]) -> set[str]:
    return {e.category for e in expenses}

def delete_expense(expense_id: str) -> bool:
    with SessionLocal() as session:
        expenses = session.get(Expense, expense_id)

        if expenses is None:
            return False
        else:
            session.delete(expenses)
            session.commit()
            return True

