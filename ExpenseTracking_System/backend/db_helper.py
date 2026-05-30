import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    if connection.is_connected():
        print("Connection is successfully")
    else:
        print("Couldn't connect to the server")

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()
    cursor.close()
    connection.close()
    print("End of execution")

def fetch_Data():
    logger.info("fetch_Data function called")
    with get_db_cursor() as cursor:
        cursor.execute("select * from expenses;")
        expenseData = cursor.fetchall()

        return expenseData

def fetch_Expenses_Datewise(expense_date):
    logger.info(f"fetch_Expenses_Datewise function called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("select * from expenses where expense_date = %s",(expense_date,))
        expenseData = cursor.fetchall()

        return expenseData

def add_Expenses(expense_date,amount,food,notes):
    logger.info(f"Adding details to the databse in function add_Expenses with {expense_date} {amount} {food} {notes}")
    with get_db_cursor(True) as cursor:
        cursor.execute("insert into expenses(expense_date,amount,category,notes) values (%s, %s, %s, %s)",
                   (expense_date,amount,food,notes))
        
def delet_Expenses(expense_date):
    logger.info(f"delet_Expenses function called with {expense_date}")
    with get_db_cursor(True) as cursor:
        cursor.execute("delete from expenses where expense_date = %s",(expense_date,))

def get_expense_summary(start_date,end_date):
    logger.info(f"get_expense_summary function called with {start_date} {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute("select category,sum(amount) as total from expenses where expense_date between %s and %s group by category",(start_date,end_date))
        expenseData = cursor.fetchall()

        return expenseData
    
def get_month_summary():
    logger.info(f"get_month_summary function called to get month wise summary")
    with get_db_cursor() as cursor:
        cursor.execute("select MONTH(expense_date) AS month, MONTHNAME(expense_date) AS month_name, SUM(amount) AS total FROM expenses GROUP BY MONTH(expense_date), MONTHNAME(expense_date) ORDER BY month;")
        expenseData = cursor.fetchall()

        return expenseData

if __name__ == "__main__":
    #data = fetch_Expenses_Datewise("2024-08-01")
    #print(data)
    #add_Expenses("2026-08-28",300,"Food","Panipuri")
    #fetch_Expenses_Datewise("2026-08-28")
    #delet_Expenses("2026-08-28")
    #fetch_Expenses_Datewise("2026-08-28")

    #data = get_expense_summary("2024-08-03","2024-08-05")
    data = get_month_summary()
    print(data)