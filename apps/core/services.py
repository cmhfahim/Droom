# core/services.py
from django.db import connection


def create_core_system_tables():
    """
    Create global system-level tables (not per company).
    These are shared across all companies.
    """
    with connection.cursor() as cursor:
        # CompanyData Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_companydata (
            company_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            real_business INT,
            address TEXT,
            phone VARCHAR(20),
            total_employees INT,
            type VARCHAR(50),
            sub_plan_id INT,
            reg_date DATE,
            supervisor_id INT
        );
        """)

        # SubscriptionPlan Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_subscriptionplan (
            sub_plan_id INT AUTO_INCREMENT PRIMARY KEY,
            type VARCHAR(50),
            name VARCHAR(100),
            price DECIMAL(12,2)
        );
        """)

        # BusinessType Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_businesstype (
            real_business INT AUTO_INCREMENT PRIMARY KEY,
            type VARCHAR(50)
        );
        """)

        # AdminStuff Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_adminstuff (
            s_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            address TEXT,
            phone VARCHAR(20),
            joining_date DATE,
            salary DECIMAL(12,2),
            post VARCHAR(50),
            type_s VARCHAR(50)
        );
        """)

        # AdminType Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_admintype (
            post VARCHAR(50) PRIMARY KEY,
            type_s VARCHAR(50)
        );
        """)

        # PaymentHistory Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_paymenthistory (
            company_id INT,
            date DATE,
            method VARCHAR(50),
            sub_plan_id INT,
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        );
        """)

        # CompanyLogin Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_companylogin (
            com_pass VARCHAR(255) PRIMARY KEY,
            company_id INT,
            password VARCHAR(255),
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        );
        """)


def register_company_tables(company_id):
    """
    Creates per-company tables dynamically after registration.
    Tables are prefixed with company{company_id}_.
    """
    tables_sql = [
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_payment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            last_pay_date DATE,
            next_pay_date DATE,
            method VARCHAR(50),
            sub_plan_id INT,
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_employee (
            emp_id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            name VARCHAR(100),
            age INT,
            address VARCHAR(200),
            phone VARCHAR(50),
            joining_date DATE,
            salary DECIMAL(10,2),
            post VARCHAR(100),
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            date DATE,
            type_id INT,
            item_id INT,
            total DECIMAL(10,2),
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_materialsexp (
            type_id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            date DATE,
            cost DECIMAL(10,2),
            item_id INT,
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_operationalexp (
            type_id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            date DATE,
            cost DECIMAL(10,2),
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_itemdata (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            buying_price DECIMAL(10,2),
            selling_price DECIMAL(10,2),
            total_quantity INT,
            total_cost DECIMAL(10,2),
            remain INT,
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_dashboard (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            item_id INT,
            remain INT,
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id),
            FOREIGN KEY (item_id) REFERENCES company{company_id}_itemdata(item_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_itemsupervisor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            item_id INT,
            emp_id INT,
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS company{company_id}_companylogintime (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            date DATE,
            time TIME,
            employee_id INT,
            FOREIGN KEY (company_id) REFERENCES core_companydata(company_id)
        )
        """
    ]

    with connection.cursor() as cursor:
        for sql in tables_sql:
            cursor.execute(sql)


def create_custom_table(company_id: int, table_name: str, attributes: dict):
    """
    Dynamically create a custom table for a company.
    Table name is prefixed with company{company_id}_.
    """
    table_name_prefixed = f"company{company_id}_{table_name}"
    columns = [f"{col} {dtype}" for col, dtype in attributes.items()]
    columns_sql = ", ".join(columns)

    sql = f"CREATE TABLE IF NOT EXISTS {table_name_prefixed} ({columns_sql});"

    with connection.cursor() as cursor:
        cursor.execute(sql)


def drop_custom_table(company_id: int, table_name: str):
    """
    Drop a custom table from a company.
    """
    table_name_prefixed = f"company{company_id}_{table_name}"
    sql = f"DROP TABLE IF EXISTS {table_name_prefixed};"

    with connection.cursor() as cursor:
        cursor.execute(sql)
