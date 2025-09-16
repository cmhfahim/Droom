from django.shortcuts import render, redirect
from apps.users.models import UserCompany
from django.contrib.auth.decorators import login_required
from .models import CompanyData, ItemData, Expenses, Dashboard

def landing(request):
    companies = CompanyData.objects.all()
    return render(request, 'core/landing.html', {'companies': companies})

@login_required
def dashboard(request):
    company = request.user.company
    items = ItemData.objects.filter(company=company)
    expenses = Expenses.objects.filter(company=company)
    return render(request, 'core/dashboard.html', {
        'company': company,
        'items': items,
        'expenses': expenses
    })

