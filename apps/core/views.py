from django.shortcuts import render, redirect
from django.contrib import messages
from .services import create_custom_table, drop_custom_table

def manage_tables(request):
    company_id = request.session.get("company_id")
    if not company_id:
        return redirect("company_login")

    if request.method == "POST":
        action = request.POST.get("action")
        table_name = request.POST.get("table_name")
        attributes_raw = request.POST.get("attributes")  # Expect format: col1:TYPE,col2:TYPE

        # Convert string to dictionary
        try:
            attributes = dict(attr.split(":") for attr in attributes_raw.split(","))
        except Exception as e:
            messages.error(request, f"Invalid attributes format. Example: name:VARCHAR(50),age:INT")
            return redirect("manage_tables")

        if action == "create":
            create_custom_table(company_id, table_name, attributes)
            messages.success(request, f"Table '{table_name}' created successfully!")
        elif action == "delete":
            drop_custom_table(company_id, table_name)
            messages.success(request, f"Table '{table_name}' deleted successfully!")

        return redirect("manage_tables")

    return render(request, "core/table_manager.html")
