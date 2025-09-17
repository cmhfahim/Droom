from django.db import models
from django.contrib.auth.models import User


# ===================== SUPPORTING TABLES =====================

class BusinessType(models.Model):
    real_business = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class SubscriptionPlan(models.Model):
    sub_plan_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class AdminType(models.Model):
    post = models.AutoField(primary_key=True)
    type_s = models.CharField(max_length=100)

    def __str__(self):
        return self.type_s


class AdminStuff(models.Model):
    s_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=50)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    post = models.ForeignKey(AdminType, on_delete=models.CASCADE)
    type_s = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ===================== MAIN COMPANY TABLE =====================

class CompanyData(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    # Instead of storing raw string/int → use relations
    real_business = models.ForeignKey(BusinessType, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    total_employees = models.IntegerField()
    type = models.CharField(max_length=100)
    sub_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    reg_date = models.DateField(auto_now_add=True)
    supervisor = models.ForeignKey(AdminStuff, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# ===================== AUTH & PAYMENTS =====================

class CompanyLogin(models.Model):
    com_pass = models.CharField(max_length=255, primary_key=True)
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)


class CompanyPayment(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    last_pay_date = models.DateField()
    next_pay_date = models.DateField()
    method = models.CharField(max_length=50)
    sub_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)


class PaymentHistory(models.Model):
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    date = models.DateField()
    method = models.CharField(max_length=50)
    sub_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)


# ===================== COMPANY BUSINESS DATA =====================

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

    def __str__(self):
        return self.name


class ItemData(models.Model):
    item_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyData, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    buying_price = models.FloatField()
    selling_price = models.FloatField()
    total_quantity = models.IntegerField()
    total_cost = models.FloatField()
    remain = models.IntegerField()

    def __str__(self):
        return self.name


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
