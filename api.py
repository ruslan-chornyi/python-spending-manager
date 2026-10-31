from fastapi import FastAPI, HTTPException, Depends, Header
from app.schemas import ExpenseCreate, ExpenseRead
from app.storage import load_expense_by_user, save_expense, delete_expense, get_user_id_by_key
from app.models import Expense
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


def get_current_user(x_api_key: str = Header()) -> int:
    user_id = get_user_id_by_key(x_api_key)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user_id


@app.get("/")
async def root():
    return {"message": "Expense API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/expenses", response_model=list[ExpenseRead])
def get_expenses(user_id: int = Depends(get_current_user)):
    return load_expense_by_user(user_id)

@app.post("/expenses", response_model=ExpenseRead, status_code=201)
async def add_expenses(expense: ExpenseCreate, user_id: int = Depends(get_current_user)):
    new_expense = Expense(name=expense.name, price=expense.price, category=expense.category, user_id=user_id)
    save_expense(new_expense)
    return new_expense

@app.delete("/expenses/{expense_id}", status_code=204)
def remove_expense(expense_id: str, user_id: int = Depends(get_current_user)):
    deleted = delete_expense(expense_id, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
