from django.db import models
from django.contrib.auth.models import User

class CompanyData(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    real_business = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    total_employees = models.IntegerField()
    type = models.CharField(max_length=50)
    sub_plan_id = models.IntegerField()
    reg_date = models.DateField(auto_now_add=True)
    supervisor_id = models.IntegerField()

class CompanyLogin(models.Model):
    com_pass = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)

# Customer company tables
class CompanyPayment(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    last_pay_date = models.DateField()
    next_pay_date = models.DateField()
    method = models.CharField(max_length=50)
    sub_plan_id = models.IntegerField()

class CompanyEmployee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    joining_date = models.DateField()
    salary = models.FloatField()
    post = models.CharField(max_length=50)

class ItemData(models.Model):
    item_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    buying_price = models.FloatField()
    selling_price = models.FloatField()
    total_quantity = models.IntegerField()
    total_cost = models.FloatField()
    remain = models.IntegerField()

class Expenses(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    date = models.DateField()
    type_id = models.CharField(max_length=50)
    item = models.ForeignKey(ItemData, on_delete=models.CASCADE)
    total = models.FloatField()

class Dashboard(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemData, on_delete=models.CASCADE)
    remain = models.IntegerField()

class ItemSupervisor(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemData, on_delete=models.CASCADE)
    employee = models.ForeignKey(CompanyEmployee, on_delete=models.CASCADE)

class CompanyLoginTime(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    employee = models.ForeignKey(CompanyEmployee, on_delete=models.CASCADE)

