from pydantic import BaseModel, ConfigDict

class ExpenseCreate(BaseModel):
    name: str
    price: int
    category: str

class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    expense_id: str
    name: str
    price: int
    category: str