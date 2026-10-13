from pydantic import BaseModel, ConfigDict

class ExpenseCreate(BaseModel):
    name: str
    price: float
    category: str

class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    expense_id: str
    name: str
    price: float
    category: str