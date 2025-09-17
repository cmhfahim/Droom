in my file i have billing file i am sharing its all code tell me if i need to do anything

billing/models.py
from django.db import models
from apps.core.models import CompanyData

class BillingHistory(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField()
    method = models.CharField(max_length=50)

billing/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_dashboard, name='billing_dashboard'),
]

billing/views.py

from django.shortcuts import render
from apps.billing.models import BillingHistory
from django.contrib.auth.decorators import login_required

@login_required
def billing_dashboard(request):
    company = request.user.company
    bills = BillingHistory.objects.filter(company=company)
    return render(request, 'billing/billing_dashboard.html', {'bills': bills})

its all my code
