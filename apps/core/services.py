from django.db import connection

def create_customer_company_tables(company_id: int):
    """
    Create the required tables for a newly registered company.
    All table names are prefixed with company_id to separate companies.
    """
    prefix = f"company_{company_id}_"

    with connection.cursor() as cursor:
        # -------------------------
        # Core company tables (prefixed)
        # -------------------------

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}CompanyData (
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

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}SubscriptionPlan (
            Sub_plan_id INT AUTO_INCREMENT PRIMARY KEY,
            Type VARCHAR(50),
            Name VARCHAR(100),
            Price DECIMAL(12,2)
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}BusinessType (
            Real_business INT AUTO_INCREMENT PRIMARY KEY,
            Type VARCHAR(50)
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}AdminStuff (
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

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}AdminType (
            Post VARCHAR(50) PRIMARY KEY,
            Type_s VARCHAR(50)
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}PaymentHistory (
            Company_id INT,
            Date DATE,
            Method VARCHAR(50),
            Sub_plan_id INT
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}CompanyLogin (
            com_pass VARCHAR(255) PRIMARY KEY,
            Company_id INT,
            Password VARCHAR(255)
        );
        """)

        # -------------------------
        # Customer company tables (prefixed)
        # -------------------------

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}CompanyPayment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Last_pay_date DATE,
            Next_pay_date DATE,
            Method VARCHAR(50),
            Sub_plan_id INT
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}CompanyEmployee (
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

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}Expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Date DATE,
            Type_id INT,
            Item_id INT,
            Total DECIMAL(12,2)
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}MaterialsExp (
            Type_id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Date DATE,
            Cost DECIMAL(12,2),
            Item_id INT
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}OperationalExp (
            Type_id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Date DATE,
            Cost DECIMAL(12,2)
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}Dashboard (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Item_id INT,
            Remain INT
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}ItemSupervisor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Item_id INT,
            Emp_id INT
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}ItemData (
            Item_id INT AUTO_INCREMENT PRIMARY KEY,
            Company_id INT NOT NULL,
            Buying_price DECIMAL(12,2),
            Selling_price DECIMAL(12,2),
            Total_quantity INT,
            Total_cost DECIMAL(12,2),
            Remain INT
        );
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {prefix}CompanyLoginTime (
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
    Table name is prefixed with company_id.
    """
    table_name_prefixed = f"company_{company_id}_{table_name}"
    columns = [f"{col} {dtype}" for col, dtype in attributes.items()]
    columns_sql = ", ".join(columns)

    sql = f"CREATE TABLE IF NOT EXISTS {table_name_prefixed} ({columns_sql});"

    with connection.cursor() as cursor:
        cursor.execute(sql)


def drop_custom_table(company_id: int, table_name: str):
    """
    Drop a custom table from a company.
    """
    table_name_prefixed = f"company_{company_id}_{table_name}"
    sql = f"DROP TABLE IF EXISTS {table_name_prefixed};"

    with connection.cursor() as cursor:
        cursor.execute(sql)
