from django.urls import include, path
from rest_framework import routers


from .views import PersonViewSet, RegistrationDateReportView, GenderReportView, JalaliYearsView


router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet, basename='person')


urlpatterns = [
    path('', include(router.urls)),
    path('registration-date-report/<int:year>/', 
         RegistrationDateReportView.as_view(), 
         name='registration-date-report'
    ),
    path('gender-report/', 
        GenderReportView.as_view(), 
        name='gender-report'
    ),
    path('jalali-years/', 
        JalaliYearsView.as_view(), 
        name='jalali-years'
    ),
]