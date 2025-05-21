from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Person
from .serializers import PersonSerializer, RegistrationDateReportSerializer
from registry.services.report_service import ReportService


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class RegistrationDateReportView(APIView):
    def get(self, request, year):
        registrations_by_month_and_week = ReportService.count_of_registrations_by_month_and_week(year)
        serializer = RegistrationDateReportSerializer(registrations_by_month_and_week)
        return Response(serializer.data)
    

class GenderReportView(APIView):
    def get(self, request):
        gender_report = ReportService.gender_counts()
        return Response(gender_report)


class JalaliYearsView(APIView):
    def get(self, request):
        years = ReportService.list_of_jalali_years()
        return Response(years)
