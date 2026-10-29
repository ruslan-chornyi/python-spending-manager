import hashlib, secrets
from app.db import Base, engine, SessionLocal
from app.models import Expense, Apikey
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

def delete_expense(expense_id: str, user_id: int | None = None) -> bool:
    with SessionLocal() as session:
        expense = session.get(Expense, expense_id)

        if expense is None:
            return False

        if user_id is not None and expense.user_id != user_id:
            return False

        session.delete(expense)
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
            .filter(Expense.user_id == user_id)
            .group_by(Expense.category)
            .order_by(func.sum(Expense.price).desc())
            .first()
        )

        if result is None:
            return None

        return result[0]

def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

def create_api_key(user_id: int) -> str:
    key = secrets.token_urlsafe(32)
    api_key = Apikey(user_id=user_id, key_hash=hash_key(key))
    with SessionLocal() as session:
        session.add(api_key)
        session.commit()
    return key

def get_user_id_by_key(key: str) -> int | None:
    with SessionLocal() as session:
        row = session.query(Apikey).filter(Apikey.key_hash == hash_key(key)).first()

        if row is None:
            return None
        return row.user_id
