from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    company_id = request.user.id  # or however you link user to company

    schema_name = f"company_{company_id}"

    with connection.cursor() as cursor:
        cursor.execute(f"USE {schema_name};")
        # Example: fetch all items for dashboard
        cursor.execute("SELECT * FROM Dashboard;")
        dashboard_items = cursor.fetchall()

    return render(request, 'core/dashboard.html', {'dashboard_items': dashboard_items})
