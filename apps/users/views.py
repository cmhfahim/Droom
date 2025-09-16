from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CompanyUser
from apps.core.services import create_customer_company_db

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        business_type = request.POST['business_type']

        # Save user/company to your user table
        user = CompanyUser.objects.create(
            name=name,
            email=email,
            password=password,  # make sure to hash
            business_type=business_type
        )

        # Call service to create dedicated DB and tables
        create_customer_company_db(user.id)

        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'users/register.html')
