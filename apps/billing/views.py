from django.shortcuts import render
from apps.billing.models import BillingHistory
from django.contrib.auth.decorators import login_required

@login_required
def billing_dashboard(request):
    company = request.user.company
    bills = BillingHistory.objects.filter(company=company)
    return render(request, 'billing/billing_dashboard.html', {'bills': bills})

