from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database
import models
import schemas

# Create database tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Daily Expense Tracker API")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/initial-balance/", response_model=schemas.InitialBalanceResponse)
def create_initial_balance(balance: schemas.InitialBalanceCreate, db: Session = Depends(get_db)):
    db_balance = models.InitialBalance(total_amount=balance.total_amount)
    db.add(db_balance)
    db.commit()
    db.refresh(db_balance)
    return db_balance

@app.get("/initial-balance/", response_model=schemas.InitialBalanceResponse)
def get_initial_balance(db: Session = Depends(get_db)):
    # Fetches the latest initial balance record
    db_balance = db.query(models.InitialBalance).order_by(models.InitialBalance.id.desc()).first()
    if not db_balance:
        raise HTTPException(status_code=404, detail="Initial balance not found")
    return db_balance

@app.put("/initial-balance/{balance_id}", response_model=schemas.InitialBalanceResponse)
def update_initial_balance(balance_id: int, balance: schemas.InitialBalanceUpdate, db: Session = Depends(get_db)):
    db_balance = db.query(models.InitialBalance).filter(models.InitialBalance.id == balance_id).first()
    if not db_balance:
        raise HTTPException(status_code=404, detail="Initial balance not found")
    
    # Pydantic V1/V2 compatibility for getting update data
    update_data = balance.model_dump(exclude_unset=True) if hasattr(balance, 'model_dump') else balance.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_balance, key, value)
        
    db.commit()
    db.refresh(db_balance)
    return db_balance

@app.post("/expenses/", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.DailyExpense(expense_for=expense.expense_for, amount=expense.amount)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses/", response_model=List[schemas.ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(models.DailyExpense).all()

@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense_by_id(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(models.DailyExpense).filter(models.DailyExpense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(models.DailyExpense).filter(models.DailyExpense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_data = expense.model_dump(exclude_unset=True) if hasattr(expense, 'model_dump') else expense.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
        
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(models.DailyExpense).filter(models.DailyExpense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


@app.post("/saving-goals/", response_model=schemas.SavingGoalResponse)
def create_saving_goal(goal: schemas.SavingGoalCreate, db: Session = Depends(get_db)):
    db_goal = models.SavingGoal(
        monthly_goal=goal.monthly_goal,
        weekly_goal=goal.weekly_goal,
        daily_goal=goal.daily_goal
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.get("/saving-goals/", response_model=schemas.SavingGoalResponse)
def get_saving_goal(db: Session = Depends(get_db)):
    # Fetches the latest saving goal record
    db_goal = db.query(models.SavingGoal).order_by(models.SavingGoal.id.desc()).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Saving goal not found")
    return db_goal

@app.put("/saving-goals/{goal_id}", response_model=schemas.SavingGoalResponse)
def update_saving_goal(goal_id: int, goal: schemas.SavingGoalUpdate, db: Session = Depends(get_db)):
    db_goal = db.query(models.SavingGoal).filter(models.SavingGoal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Saving goal not found")
    
    update_data = goal.model_dump(exclude_unset=True) if hasattr(goal, 'model_dump') else goal.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_goal, key, value)
        
    db.commit()
    db.refresh(db_goal)
    return db_goal