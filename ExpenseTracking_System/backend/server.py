from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()

class ExpenseModel(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/expenses/{expense_date}", response_model=List[ExpenseModel]) 
def get_expenses(expense_date: date):
    expense_data = db_helper.fetch_Expenses_Datewise(expense_date)
    return expense_data

@app.post("/expenses/{expense_date}") 
def add_update_expenses(expense_date: date,expenses:List[ExpenseModel]):
    db_helper.delet_Expenses(expense_date)
    for expense in expenses:
        db_helper.add_Expenses(expense_date,expense.amount,expense.category,expense.notes)
    
    return "Expense updated successfully"

@app.post("/analytics") 
def get_range(date_range: DateRange):
    expense_data = db_helper.get_expense_summary(date_range.start_date,date_range.end_date)

    if expense_data is None:
        raise HTTPException(status_code=500,detail="Failed to extract expense summary from the database.")

    total_amount = sum([row['total'] for row in expense_data])

    breakdown_dict = {}
    for row in expense_data:
        percentage = (row['total']/total_amount)*100 if total_amount != 0 else 0
        breakdown_dict[row['category']] = {
            "total" : row['total'],
            "percentage" : round(percentage, 2)
        }

    return breakdown_dict

@app.post("/analystics_month")
def get_month_details():
    expense_data = db_helper.get_month_summary()

    if expense_data is None:
        raise HTTPException(status_code=500,detail="Failed to extract month wise expense summary from the database.")

  
    breakdown_dict = {}
    for row in expense_data:
        breakdown_dict[row['month']] = {
            "month_name" : row['month_name'],
            "total" : row['total']
        }

    return breakdown_dict