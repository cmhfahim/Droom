# core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required

from .forms import CompanyRegistrationForm, CompanyLoginForm
from .services import register_company_tables, create_custom_table, drop_custom_table
from .models import CompanyData, CompanyLogin

# ---------------------------
# Company Registration
# ---------------------------
def register_company_view(request):
    """
    Handles new company registration and auto-creates their prefixed tables.
    """
    if request.method == "POST":
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save()
            # Create company-specific tables
            register_company_tables(company.company_id)
            messages.success(request, "Company registered successfully!")
            return redirect("dashboard", company_id=company.company_id)
    else:
        form = CompanyRegistrationForm()

    return render(request, "core/register_company.html", {"form": form})


# ---------------------------
# Company Login
# ---------------------------
def company_login(request):
    """
    Login view for companies using company_id and password.
    """
    if request.method == "POST":
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            company_id = form.cleaned_data["company_id"]
            password = form.cleaned_data["password"]

            try:
                login_record = CompanyLogin.objects.get(company__company_id=company_id, password=password)
                request.user.company_id = company_id  # Set company_id in session-like user attribute
                messages.success(request, "Login successful!")
                return redirect("dashboard")
            except CompanyLogin.DoesNotExist:
                messages.error(request, "Invalid company ID or password.")
    else:
        form = CompanyLoginForm()
    return render(request, "core/company_login.html", {"form": form})


# ---------------------------
# Dashboard
# ---------------------------
@login_required
def dashboard(request, company_id=None):
    """
    Shows company dashboard: employees, expenses, items, summary dashboard.
    Supports both request.user.company_id (if logged in) or company_id from URL.
    """
    if company_id is None:
        company_id = getattr(request.user, "company_id", None)

    if not company_id:
        messages.error(request, "Company not identified. Please log in again.")
        return redirect("company_login")

    data = {
        "employees": [],
        "expenses": [],
        "items": [],
        "dashboard": [],
        "company_id": company_id,
    }

    try:
        with connection.cursor() as cursor:
            # Employees
            cursor.execute(f"SELECT * FROM company{company_id}_employee")
            data["employees"] = cursor.fetchall()

            # Expenses
            cursor.execute(f"SELECT * FROM company{company_id}_expenses")
            data["expenses"] = cursor.fetchall()

            # Items
            cursor.execute(f"SELECT * FROM company{company_id}_itemdata")
            data["items"] = cursor.fetchall()

            # Dashboard summary
            cursor.execute(f"SELECT * FROM company{company_id}_dashboard")
            data["dashboard"] = cursor.fetchall()

    except Exception as e:
        messages.error(request, f"Error fetching dashboard data: {e}")

    return render(request, "core/dashboard.html", data)


# ---------------------------
# Dynamic Table Management
# ---------------------------
@login_required
def manage_tables(request):
    """
    Allow a company to dynamically create or delete custom tables
    in their database without writing SQL code.
    """
    company_id = getattr(request.user, "company_id", None)
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
