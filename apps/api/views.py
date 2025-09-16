from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.api.serializers import CompanySerializer
from apps.core.models import CompanyData

class CompanyListAPI(APIView):
    def get(self, request):
        companies = CompanyData.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

