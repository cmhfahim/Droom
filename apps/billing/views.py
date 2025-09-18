from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.billing.models import BillingHistory
from apps.core.models import CompanyData

@login_required
def billing_dashboard(request):
    """
    Display billing history for the company associated with the logged-in user.
    """
    # Get company ID from user
    company_id = getattr(request.user, "company_id", None)
    
    if not company_id:
        messages.error(request, "Company not identified. Please log in again.")
        return redirect("users:login")  # Redirect to login page

    try:
        company = CompanyData.objects.get(pk=company_id)
    except CompanyData.DoesNotExist:
        messages.error(request, "Company does not exist.")
        return redirect("users:login")
    
    # Fetch billing history for this company
    bills = BillingHistory.objects.filter(company=company).order_by('-date')

    return render(request, 'billing/billing_dashboard.html', {'bills': bills, 'company': company})
