from django.db import models
from apps.core.models import CompanyData

class BillingHistory(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField()
    method = models.CharField(max_length=50)

