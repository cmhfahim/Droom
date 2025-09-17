# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path("", views.landing, name="landing"),

    # Company registration & login
    path("register/", views.register_company_view, name="register_company"),
    path("login/", views.company_login, name="company_login"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),  # Uses request.user.company_id
    path("dashboard/<int:company_id>/", views.dashboard, name="dashboard_with_id"),  # Explicit company_id

    # Manage tables (create/delete without SQL)
    path("tables/manage/", views.manage_tables, name="manage_tables"),
]
