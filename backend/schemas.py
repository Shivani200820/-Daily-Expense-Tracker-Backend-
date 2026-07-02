from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

class InitialBalanceBase(BaseModel):
    total_amount: Decimal

class InitialBalanceCreate(InitialBalanceBase):
    pass

class InitialBalanceUpdate(BaseModel):
    total_amount: Optional[Decimal] = None

class InitialBalanceResponse(InitialBalanceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic V2
        orm_mode = True         # Pydantic V1

class ExpenseBase(BaseModel):
    expense_for: str
    amount: Decimal

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    expense_for: Optional[str] = None
    amount: Optional[Decimal] = None

class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class SavingGoalBase(BaseModel):
    monthly_goal: Decimal
    weekly_goal: Decimal
    daily_goal: Decimal

class SavingGoalCreate(SavingGoalBase):
    pass

class SavingGoalUpdate(BaseModel):
    monthly_goal: Optional[Decimal] = None
    weekly_goal: Optional[Decimal] = None
    daily_goal: Optional[Decimal] = None

class SavingGoalResponse(SavingGoalBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True