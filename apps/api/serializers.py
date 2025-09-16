from rest_framework import serializers
from apps.core.models import CompanyData

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyData
        fields = '__all__'

