from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = "Kullanıcı"

class BudgetUpdate(BaseModel):
    monthly_budget: float

class Token(BaseModel):
    access_token: str
    token_type: str

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: Optional[str] = None

class SmartExpenseCreate(BaseModel):
    raw_text: str

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    is_ai_categorized: bool
    created_at: datetime

    class Config:
        from_attributes = True