from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from .services import create_custom_table, drop_custom_table

@login_required
def dashboard(request):
    """
    Show the company dashboard: items, employees, expenses, materials, operational expenses.
    """
    company_id = request.user.company_id  # Each user belongs to a company
    schema_name = f"company_{company_id}"

    # Initialize dashboard data dictionary
    dashboard_data = {
        "items": [],
        "employees": [],
        "expenses": [],
        "materials": [],
        "operations": [],
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"USE {schema_name};")

            # Fetch dashboard items
            cursor.execute("SELECT * FROM ItemData;")
            dashboard_data['items'] = cursor.fetchall()

            # Fetch employees
            cursor.execute("SELECT * FROM CompanyEmployee;")
            dashboard_data['employees'] = cursor.fetchall()

            # Fetch expenses
            cursor.execute("SELECT * FROM Expenses;")
            dashboard_data['expenses'] = cursor.fetchall()

            # Fetch materials
            cursor.execute("SELECT * FROM MaterialsExp;")
            dashboard_data['materials'] = cursor.fetchall()

            # Fetch operational expenses
            cursor.execute("SELECT * FROM OperationalExp;")
            dashboard_data['operations'] = cursor.fetchall()

    except Exception as e:
        messages.error(request, f"Error fetching dashboard data: {e}")

    return render(request, "core/dashboard.html", {"dashboard_data": dashboard_data})


@login_required
def manage_tables(request):
    """
    Allow a company to dynamically create or delete tables in their database
    without writing SQL code.
    """
    company_id = request.user.company_id
    if not company_id:
        messages.error(request, "Company not identified. Please log in again.")
        return redirect("company_login")

    if request.method == "POST":
        action = request.POST.get("action")
        table_name = request.POST.get("table_name")
        attributes_raw = request.POST.get("attributes")  # Format: col1:TYPE,col2:TYPE

        if not table_name or not attributes_raw:
            messages.error(request, "Both table name and attributes are required.")
            return redirect("manage_tables")

        try:
            attributes = {}
            for pair in attributes_raw.split(","):
                col, dtype = pair.split(":")
                attributes[col.strip()] = dtype.strip()
        except Exception:
            messages.error(
                request,
                "Invalid attributes format. Example: name:VARCHAR(50),age:INT"
            )
            return redirect("manage_tables")

        try:
            if action == "create":
                create_custom_table(company_id, table_name, attributes)
                messages.success(request, f"Table '{table_name}' created successfully!")
            elif action == "delete":
                drop_custom_table(company_id, table_name)
                messages.success(request, f"Table '{table_name}' deleted successfully!")
            else:
                messages.error(request, "Invalid action selected.")
        except Exception as e:
            messages.error(request, f"Error executing action: {e}")

        return redirect("manage_tables")

    return render(request, "core/table_manager.html")
