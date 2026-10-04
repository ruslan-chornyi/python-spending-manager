from app.db import Base, engine, SessionLocal
from app.models import Expense
from sqlalchemy import func

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

def load_expense_by_category(category: str) -> list[Expense]:
    with SessionLocal() as session:
        return session.query(Expense).filter(Expense.category == category).all()

def load_expense_by_user_and_category(user_id: int, category: str) -> list[Expense]:
    with SessionLocal() as session:
        return session.query(Expense).filter(Expense.user_id == user_id, Expense.category == category).all()

def count_expense_by_user(user_id: int) -> int:
    with SessionLocal() as session:
        return session.query(Expense).filter(Expense.user_id == user_id).count()

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

def total_spent_by_user(user_id: int) -> int:
    with SessionLocal() as session:
        return session.query(func.sum(Expense.price)).filter(Expense.user_id == user_id).scalar()

def load_expenses_sorted_by_price(user_id: int, descending: bool = False) -> list[Expense]:
    with SessionLocal() as session:
        if descending:
            return session.query(Expense).order_by(Expense.price.desc()).filter(Expense.user_id == user_id).all()
        else:
            return session.query(Expense).order_by(Expense.price).filter(Expense.user_id == user_id).all()

def most_expensive_category(user_id: int) -> str | None:
    with SessionLocal() as session:
        result = (
            session.query(Expense.category, func.sum(Expense.price))
            .group_by(Expense.category)
            .order_by(func.sum(Expense.price).desc())
            .filter(Expense.user_id == user_id)
            .first()
        )

        if result is None:
            return None

        return result[0]