# core/forms.py
from django import forms
from .models import CompanyData


# ✅ Company Registration Form
class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = CompanyData
        fields = [
            "name",
            "real_business",
            "address",
            "phone",
            "total_employees",
            "type",
            "sub_plan",
            "supervisor",
        ]


# ✅ Company Login Form
class CompanyLoginForm(forms.Form):
    company_id = forms.IntegerField(label="Company ID")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
