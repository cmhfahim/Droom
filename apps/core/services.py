from django.db import connection


def create_customer_company_db(company_id: int):
    """
    Creates the required schema/tables for a newly registered company.
    Each company gets its own schema (database) with predefined tables.
    """
    schema_name = f"company_{company_id}"

    with connection.cursor() as cursor:
        # Create schema
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {schema_name};")
        cursor.execute(f"USE {schema_name};")

        # -------------------------
        # Core system tables
        # -------------------------

        # CompanyData Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanyData (
            Company_id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Real_business INT,
            Address TEXT,
            Phone VARCHAR(20),
            Total_employees INT,
            Type VARCHAR(50),
            Sub_plan_id INT,
            Reg_date DATE,
            Supervisor_id INT
        );
        """)

        # SubscriptionPlan Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS SubscriptionPlan (
            Sub_plan_id INT AUTO_INCREMENT PRIMARY KEY,
            Type VARCHAR(50),
            Name VARCHAR(100),
            Price DECIMAL(12,2)
        );
        """)

        # BusinessType Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS BusinessType (
            Real_business INT AUTO_INCREMENT PRIMARY KEY,
            Type VARCHAR(50)
        );
        """)

        # AdminStuff Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS AdminStuff (
            S_id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100),
            Age INT,
            Address TEXT,
            Phone VARCHAR(20),
            Joining_date DATE,
            Salary DECIMAL(12,2),
            Post VARCHAR(50),
            Type_s VARCHAR(50)
        );
        """)

        # AdminType Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS AdminType (
            Post VARCHAR(50) PRIMARY KEY,
            Type_s VARCHAR(50)
        );
        """)

        # PaymentHistory Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS PaymentHistory (
            Company_id INT,
            Date DATE,
            Method VARCHAR(50),
            Sub_plan_id INT
        );
        """)

        # CompanyLogin Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanyLogin (
            com_pass VARCHAR(255) PRIMARY KEY,
            Company_id INT,
            Password VARCHAR(255)
        );
        """)

        # -------------------------
        # Customer company tables
        # -------------------------

        # Company Payment Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanyPayment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Last_pay_date DATE,
            Next_pay_date DATE,
            Method VARCHAR(50),
            Sub_plan_id INT
        );
        """)

        # Company Employee Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanyEmployee (
            Emp_id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Name VARCHAR(100),
            Age INT,
            Address TEXT,
            Phone VARCHAR(20),
            Joining_date DATE,
            Salary DECIMAL(12,2),
            Post VARCHAR(100)
        );
        """)

        # Expenses Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Date DATE,
            Type_id INT,
            Item_id INT,
            Total DECIMAL(12,2)
        );
        """)

        # Materials Expenses Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MaterialsExp (
            Type_id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Date DATE,
            Cost DECIMAL(12,2),
            Item_id INT
        );
        """)

        # Operational Expenses Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OperationalExp (
            Type_id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Date DATE,
            Cost DECIMAL(12,2)
        );
        """)

        # Dashboard Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dashboard (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Item_id INT,
            Remain INT
        );
        """)

        # Item Supervisor Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ItemSupervisor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Item_id INT,
            Emp_id INT
        );
        """)

        # Item Data Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ItemData (
            Item_id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Buying_price DECIMAL(12,2),
            Selling_price DECIMAL(12,2),
            Total_quantity INT,
            Total_cost DECIMAL(12,2),
            Remain INT
        );
        """)

        # Company Login Time Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanyLoginTime (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Date DATE,
            Time TIME,
            Employee_id INT
        );
        """)


def create_custom_table(company_id: int, table_name: str, attributes: dict):
    """
    Dynamically create a custom table for a company.
    attributes = { "column_name": "DATA_TYPE", "column2": "DATA_TYPE" }
    """
    schema_name = f"company_{company_id}"

    columns = [f"{col} {dtype}" for col, dtype in attributes.items()]
    columns_sql = ", ".join(columns)

    sql = f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns_sql});"

    with connection.cursor() as cursor:
        cursor.execute(sql)


def drop_custom_table(company_id: int, table_name: str):
    """
    Drop a custom table from a company's schema.
    """
    schema_name = f"company_{company_id}"
    sql = f"DROP TABLE IF EXISTS {schema_name}.{table_name};"

    with connection.cursor() as cursor:
        cursor.execute(sql)
