import uuid
from sqlalchemy import Column, String, Integer, BigInteger
from app.db import Base


class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String, nullable=False)

    def __str__(self) -> str:
        return f"{self.name} cost {self.price}$ in -{self.category}- category\n"

    def __repr__(self) -> str:
        return f"Expense(expense_id={self.expense_id}, user_id={self.user_id}, name='{self.name}', price={self.price}, category='{self.category}')"