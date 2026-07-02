from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from database import Base

class InitialBalance(Base):
    __tablename__ = "initial_balances"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DailyExpense(Base):
    __tablename__ = "daily_expenses"

    id = Column(Integer, primary_key=True, index=True)
    expense_for = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SavingGoal(Base):
    __tablename__ = "saving_goals"

    id = Column(Integer, primary_key=True, index=True)
    monthly_goal = Column(Numeric(10, 2), nullable=False)
    weekly_goal = Column(Numeric(10, 2), nullable=False)
    daily_goal = Column(Numeric(10, 2), nullable=False)