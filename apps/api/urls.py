from django.urls import path
from .views import CompanyListAPI

urlpatterns = [
    path('companies/', CompanyListAPI.as_view(), name='api_companies'),
]

