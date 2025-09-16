from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import CompanyData

class UserCompany(AbstractUser):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE, null=True, blank=True)
