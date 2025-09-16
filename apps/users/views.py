from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserCompany
from apps.core.models import CompanyData
from apps.core.services import create_company_tables

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        company_name = request.POST['company_name']
        company = CompanyData.objects.create(name=company_name)
        user = UserCompany.objects.create_user(username=username, password=password, company=company)
        create_company_tables(company)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'users/login.html')
