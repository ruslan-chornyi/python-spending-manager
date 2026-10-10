from fastapi import FastAPI
from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    name: str
    price: float
    category: str

app = FastAPI()

FAKE_EXPENSES = [
    {"name": "Coffee", "price": 45, "category": "food"},
    {"name": "Bus ticket", "price": 40, "category": "transport"},
    {"name": "Pizza", "price": 180, "category": "food"},
    {"name": "Taxi", "price": 220, "category": "transport"},
    {"name": "Book", "price": 300, "category": "education"},
]

@app.get("/")
async def root():
    return {"message": "Expense API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/fake-expenses")
async def fake_expenses(category: str | None = None, limit: int = 10):
    result = FAKE_EXPENSES

    if category is not None:
        result = [e for e in FAKE_EXPENSES if e["category"] == category]
    result = result[:limit]

    return result

@app.post("/fake-expenses")
async def add_fake_expenses(expense: ExpenseCreate):

    data = expense.model_dump()
    FAKE_EXPENSES.append(data)

    return data