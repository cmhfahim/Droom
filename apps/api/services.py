from django.db import connection
from datetime import datetime

# -------------------------
# Customer Company DB Services
# -------------------------

def fetch_company_billing(company_id: int):
    """
    Fetch billing data for a company.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Last_pay_date, Next_pay_date, Method, Sub_plan_id
            FROM company_%s.CompanyPayment
            ORDER BY Last_pay_date DESC
        """, [company_id])
        rows = cursor.fetchall()

    bills = [
        {
            "date": row[0],
            "next_date": row[1],
            "method": row[2],
            "sub_plan_id": row[3]
        } for row in rows
    ]
    return bills


def fetch_company_dashboard(company_id: int):
    """
    Fetch dashboard data (items and remaining quantities)
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Item_id, Remain
            FROM company_%s.Dashboard
        """, [company_id])
        rows = cursor.fetchall()

    dashboard_items = [
        {"item_id": row[0], "remain": row[1]} for row in rows
    ]
    return dashboard_items


def add_custom_table(company_id: int, table_name: str, attributes: dict):
    """
    Dynamically create a new custom table for a company.
    attributes = { "column_name": "DATA_TYPE", "column2": "DATA_TYPE" }
    """
    columns = [f"{col} {dtype}" for col, dtype in attributes.items()]
    columns_sql = ", ".join(columns)
    sql = f"CREATE TABLE IF NOT EXISTS company_{company_id}.{table_name} ({columns_sql});"

    with connection.cursor() as cursor:
        cursor.execute(sql)
    return f"Table {table_name} created successfully for company {company_id}"


def remove_custom_table(company_id: int, table_name: str):
    """
    Drop a custom table from a company's database
    """
    sql = f"DROP TABLE IF EXISTS company_{company_id}.{table_name};"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    return f"Table {table_name} dropped successfully for company {company_id}"


# -------------------------
# Utility functions
# -------------------------

def get_current_datetime():
    """Return current datetime in YYYY-MM-DD HH:MM:SS format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

